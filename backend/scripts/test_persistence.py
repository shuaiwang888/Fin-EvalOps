#!/usr/bin/env python3
"""Local smoke test for `app.persistence` — does not start the FastAPI app.

Runs three checks:
  1) Configuration check: are HF_TOKEN / HF_NAMESPACE / HF_DATASET_REPO set?
  2) `pull_db(force=True)` — downloads fin_evalops.db from the Dataset repo
     to a temp path, verifies it's a valid SQLite file.
  3) `push_db(reason='local-test', force=True)` — backs up the local DB and
     uploads it; verifies the file ends up in the Dataset repo.

Usage:
    # 1. Quick: skip push (just verify config + pull)
    python backend/scripts/test_persistence.py --no-push

    # 2. Full: pull + push (uses your real HF_TOKEN from env)
    python backend/scripts/test_persistence.py

    # 3. Custom repo
    HF_DATASET_REPO=my-test-db python backend/scripts/test_persistence.py

Notes:
    - This script MUTATES the Dataset repo (creates/updates a commit). Use a
      throwaway `HF_DATASET_REPO` for the first run.
    - Requires `huggingface-hub` (added to backend/requirements.txt).
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

# Make `app` importable regardless of where this script is run from
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from app import persistence  # noqa: E402
from app.config import settings  # noqa: E402


# ---------------------------------------------------------------------------
def _print_status() -> None:
    print("=" * 60)
    print("Fin-EvalOps HF persistence — local smoke test")
    print("=" * 60)
    print(f"  HF_TOKEN         : {'set (' + settings.hf_token[:6] + '...)' if settings.hf_token else '<empty>'}")
    print(f"  HF_NAMESPACE     : {settings.hf_namespace or '<empty>'}")
    print(f"  HF_DATASET_REPO  : {settings.hf_dataset_repo or '<empty>'}")
    print(f"  HF_PUSH_INTERVAL : {settings.hf_push_interval}s")
    print(f"  local DB path    : {settings.db_path_abs}")
    print(f"  local DB exists  : {Path(settings.db_path_abs).exists()}")
    if Path(settings.db_path_abs).exists():
        print(f"  local DB size    : {Path(settings.db_path_abs).stat().st_size:,} bytes")
    print()


def _check_config() -> bool:
    missing = []
    if not settings.hf_token:
        missing.append("HF_TOKEN")
    if not settings.hf_namespace:
        missing.append("HF_NAMESPACE")
    if not settings.hf_dataset_repo:
        missing.append("HF_DATASET_REPO")
    if missing:
        print(f"❌ Missing required env vars: {', '.join(missing)}")
        print("   Export them and retry, e.g.:")
        print("     export HF_TOKEN=hf_xxx")
        print("     export HF_NAMESPACE=yourname")
        return False
    return True


def _check_sqlite(path: Path) -> bool:
    try:
        con = sqlite3.connect(str(path))
        cur = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        con.close()
        print(f"   valid SQLite, {len(tables)} tables: {', '.join(tables[:6])}{'...' if len(tables) > 6 else ''}")
        return True
    except Exception as exc:
        print(f"   ❌ not a valid SQLite file: {exc}")
        return False


def _download_to_temp() -> Path | None:
    """Download via huggingface_hub to a temp path (bypasses local DB)."""
    from huggingface_hub import hf_hub_download
    tmp = Path(tempfile.mkdtemp(prefix="hf_pull_"))
    try:
        path = hf_hub_download(
            repo_id=f"{settings.hf_namespace}/{settings.hf_dataset_repo}",
            filename="fin_evalops.db",
            repo_type="dataset",
            token=settings.hf_token,
            local_dir=str(tmp),
        )
        p = Path(path)
        print(f"   downloaded to {p}  ({p.stat().st_size:,} bytes)")
        return p
    except Exception as exc:
        print(f"   download failed: {type(exc).__name__}: {exc}")
        shutil.rmtree(tmp, ignore_errors=True)
        return None


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--no-push", action="store_true", help="skip the push step (pull only)")
    ap.add_argument("--no-pull", action="store_true", help="skip the pull step (push only)")
    args = ap.parse_args()

    _print_status()

    if not _check_config():
        return 1

    failures = 0

    # ---- 1) pull ----
    if not args.no_pull:
        print("📥 Step 1/3: pull fin_evalops.db from HF Dataset repo")
        # Use the helper that bypasses local-DB-exists guard (we want to test
        # even if the local DB is already populated).
        print("   testing raw huggingface_hub download…")
        p = _download_to_temp()
        if not p:
            print("   (This is OK on first deploy — Dataset repo may not exist yet.)")
        else:
            _check_sqlite(p)
            shutil.rmtree(p.parent, ignore_errors=True)
        print()

    # ---- 2) push via persistence.push_db ----
    if not args.no_push:
        if not Path(settings.db_path_abs).exists():
            print("⚠️  Step 2/3: local DB missing; creating a minimal test DB first")
            Path(settings.db_path_abs).parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(settings.db_path_abs))
            con.execute("CREATE TABLE IF NOT EXISTS _smoke_test (ts TEXT, msg TEXT)")
            con.execute("INSERT INTO _smoke_test VALUES (datetime('now'), 'local smoke test')")
            con.commit()
            con.close()
            print(f"   created {settings.db_path_abs} with a _smoke_test row")
        else:
            print(f"   using existing local DB ({Path(settings.db_path_abs).stat().st_size:,} bytes)")

        print("📤 Step 2/3: push_db(reason='local-test', force=True)")
        ok = persistence.push_db(reason="local-test", force=True)
        print(f"   result: {'✅ ok' if ok else '❌ failed'}")
        if not ok:
            failures += 1
        print()

    # ---- 3) status ----
    print("📊 Step 3/3: persistence_status snapshot")
    from huggingface_hub import HfApi
    try:
        api = HfApi(token=settings.hf_token)
        files = api.list_repo_files(
            repo_id=f"{settings.hf_namespace}/{settings.hf_dataset_repo}",
            repo_type="dataset",
        )
        print(f"   files in {settings.hf_namespace}/{settings.hf_dataset_repo}: {files}")
    except Exception as exc:
        print(f"   could not list files: {type(exc).__name__}: {exc}")

    print()
    print("=" * 60)
    if failures:
        print(f"❌ {failures} step(s) failed")
    else:
        print("✅ all steps passed")
    print("=" * 60)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
