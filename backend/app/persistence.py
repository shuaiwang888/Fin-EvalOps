"""Hugging Face Datasets persistence layer.

Fin-EvalOps deploys as a Docker-SDK Hugging Face Space, where the container
disk is **ephemeral** (lost on restart / sleep-wake / redeploy). We persist
the SQLite DB to a private HF Dataset repo:

    repo_id   = f"{HF_NAMESPACE}/{HF_DATASET_REPO}"   (repo_type="dataset")
    file path = "fin_evalops.db"

Strategy
--------
- **PULL** on startup: download latest snapshot from HF → local file
  (only if local DB is missing/empty, to avoid clobbering dev data)
- **PUSH** on:
    * `evaluate_batch` completion (once per batch — the natural unit of work)
    * app shutdown (lifespan)
    * periodic background thread (default 300 s, configurable)
- Writes call `mark_dirty()` (a cheap bool flip). Only the threads above
  actually upload. Prevents per-row commits from spamming the HF API.
- PUSH uses the SQLite online backup API (sqlite3.Connection.backup) to
  produce a consistent snapshot without blocking writers.
- If `HF_TOKEN` is empty, all persistence calls are no-ops (local-only mode).
- Single-flight via `threading.Lock` — concurrent flush calls are coalesced.
"""
from __future__ import annotations

import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import settings
from .db import DATABASE_URL, engine

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config check — read os.environ LIVE so changes (e.g. Space Secrets edited
# via the HF UI) take effect without a process restart. Falls back to
# cached settings values for tooling that runs without env.
# ---------------------------------------------------------------------------
def _env(name: str, default: str = "") -> str:
    direct = os.environ.get(name)
    if direct:
        return direct
    # Pydantic loads `.env` into lower-case Settings attributes; it does not
    # necessarily populate os.environ. Prefer a live property when present,
    # then fall back to the cached field so local persistence works too.
    live_attr = f"{name.lower()}_live"
    if hasattr(settings, live_attr):
        value = getattr(settings, live_attr)
        if value:
            return str(value)
    return str(getattr(settings, name.lower(), default) or default)


def _hf_configured() -> bool:
    return bool(_env("HF_TOKEN")) and bool(_env("HF_NAMESPACE")) and bool(_env("HF_DATASET_REPO"))


def _repo_id() -> str:
    return f"{_env('HF_NAMESPACE')}/{_env('HF_DATASET_REPO')}"


# ---------------------------------------------------------------------------
# Dirty flag (writer-side)
# ---------------------------------------------------------------------------
_dirty = False
_dirty_lock = threading.Lock()


def mark_dirty() -> None:
    """Mark the DB as having unwritten changes. Idempotent + cheap."""
    if not _hf_configured():
        return
    global _dirty
    with _dirty_lock:
        _dirty = True


def is_dirty() -> bool:
    with _dirty_lock:
        return _dirty


# ---------------------------------------------------------------------------
# Pull (reader-side, runs at startup)
# ---------------------------------------------------------------------------
def pull_db(force: bool = False) -> bool:
    """Download the latest DB from HF Dataset repo to local DB_PATH.

    Returns True if a DB was downloaded and written to disk.
    Skips silently if HF is not configured or local DB already has data
    (unless `force=True`).
    """
    if not _hf_configured():
        log.info("HF persistence not configured (HF_TOKEN/HF_NAMESPACE/HF_DATASET_REPO), skipping pull")
        return False

    local_path = Path(settings.db_path_abs)
    if local_path.exists() and local_path.stat().st_size > 100 and not force:
        log.info(
            "Local DB already has %d bytes at %s, skipping pull (set force=True to override)",
            local_path.stat().st_size, local_path,
        )
        return False

    # Ensure parent dir exists (HF Space container writeable locations)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    from huggingface_hub import hf_hub_download
    try:
        # Download into a sibling temp path first to avoid partial writes
        cache_path = hf_hub_download(
            repo_id=_repo_id(),
            filename="fin_evalops.db",
            repo_type="dataset",
            token=_env("HF_TOKEN"),
        )
        src = Path(cache_path)
        # Atomic-ish replace
        local_path.write_bytes(src.read_bytes())
        size_kb = local_path.stat().st_size / 1024
        log.info("✅ Pulled DB from HF: %s (%.1f KB)", local_path, size_kb)
        global _dirty
        with _dirty_lock:
            _dirty = False
        return True
    except Exception as exc:
        # Most common case: dataset repo doesn't exist yet (first deploy)
        err_name = type(exc).__name__
        log.warning("HF pull skipped (%s): %s", err_name, exc)
        return False


# ---------------------------------------------------------------------------
# Push (writer-side, runs after batch/shutdown/periodic)
# ---------------------------------------------------------------------------
_upload_lock = threading.Lock()  # single-flight upload


def _snapshot_to(target_path: Path) -> None:
    """Use SQLite's online backup API to safely snapshot the live DB."""
    if not DATABASE_URL.startswith("sqlite"):
        raise RuntimeError(f"persistence.push_db only supports sqlite, got: {DATABASE_URL}")

    # Acquire a connection from the pool, then use its raw driver connection
    with engine.connect() as conn:
        raw: sqlite3.Connection = conn.connection.driver_connection
        # `backup()` performs a safe online snapshot; consistent even under writes
        with sqlite3.connect(str(target_path)) as target:
            raw.backup(target, pages=0)  # pages=0 ⇒ copy in one go


def push_db(reason: str = "manual", force: bool = False) -> bool:
    """Upload the local DB to HF Dataset repo. No-op if not dirty or not configured.

    Args:
        reason: short label appended to the auto-generated commit message.
        force: upload even if the dirty flag is False (e.g. from CLI).
    """
    if not _hf_configured():
        log.debug("HF not configured, push_db is a no-op")
        return False

    with _upload_lock:
        global _dirty
        with _dirty_lock:
            if not _dirty and not force:
                log.debug("DB not dirty, skipping push (reason=%s)", reason)
                return False

        from huggingface_hub import HfApi
        api = HfApi(token=_env("HF_TOKEN"))

        local_path = Path(settings.db_path_abs)
        if not local_path.exists() or local_path.stat().st_size == 0:
            log.warning("Local DB missing/empty, nothing to push")
            return False

        snap_path = local_path.with_suffix(".db.snap")
        try:
            _snapshot_to(snap_path)
            size_mb = snap_path.stat().st_size / 1024 / 1024

            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            api.upload_file(
                path_or_fileobj=str(snap_path),
                path_in_repo="fin_evalops.db",
                repo_id=_repo_id(),
                repo_type="dataset",
                commit_message=f"auto-save {ts} ({reason})",
            )
            log.info("✅ Pushed DB to HF (%s, %.2f MB)", reason, size_mb)
            with _dirty_lock:
                _dirty = False
            return True
        except Exception as exc:
            log.exception("HF push failed (reason=%s): %s", reason, exc)
            return False
        finally:
            try:
                snap_path.unlink(missing_ok=True)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Periodic background pusher
# ---------------------------------------------------------------------------
_pusher_thread: Optional[threading.Thread] = None
_stop_event = threading.Event()


def _pusher_loop(interval: int) -> None:
    log.info("HF pusher loop started (interval=%ds)", interval)
    while not _stop_event.wait(interval):
        try:
            push_db(reason="periodic")
        except Exception:
            log.exception("Periodic push error (non-fatal)")


def start_pusher(interval: Optional[int] = None) -> None:
    """Start the background periodic pusher. Idempotent."""
    global _pusher_thread
    if not _hf_configured():
        return
    if settings.hf_push_interval_live <= 0:
        log.info("HF pusher disabled (HF_PUSH_INTERVAL=0)")
        return
    if _pusher_thread and _pusher_thread.is_alive():
        return
    _stop_event.clear()
    iv = interval if interval is not None else settings.hf_push_interval_live
    t = threading.Thread(
        target=_pusher_loop, args=(iv,), daemon=True, name="hf-db-pusher",
    )
    t.start()
    _pusher_thread = t
    log.info("Started HF pusher (interval=%ds)", iv)


def stop_pusher(timeout: float = 5.0) -> None:
    """Signal the pusher to stop and wait briefly for it to exit."""
    global _pusher_thread
    _stop_event.set()
    if _pusher_thread and _pusher_thread.is_alive():
        _pusher_thread.join(timeout=timeout)
    _pusher_thread = None


# ---------------------------------------------------------------------------
# CLI helper — for manual debugging: `python -m app.persistence pull|push`
# ---------------------------------------------------------------------------
if __name__ == "__main__":  # pragma: no cover
    import sys
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "pull":
        ok = pull_db(force="--force" in sys.argv)
        print("pull:", "ok" if ok else "skipped/failed")
    elif cmd == "push":
        ok = push_db(reason="cli", force=True)
        print("push:", "ok" if ok else "skipped/failed")
    elif cmd == "status":
        print("configured:", _hf_configured())
        print("repo_id:    ", _repo_id() if _hf_configured() else "<n/a>")
        print("dirty:      ", is_dirty())
        print("local_db:   ", settings.db_path_abs,
              f"({Path(settings.db_path_abs).stat().st_size} bytes)"
              if Path(settings.db_path_abs).exists() else "(missing)")
    else:
        print(__doc__)
        sys.exit(1)
