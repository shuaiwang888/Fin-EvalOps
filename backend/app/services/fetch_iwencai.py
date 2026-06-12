"""Thin wrapper around the existing fetch_eval_record.py.

We import the script's functions directly so we never duplicate parsing logic
or hard-code the iwencai backend URL inside backend/app/.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import List, Tuple

from ..config import settings
from ..utils.trace import get_logger

log = get_logger(__name__)

_module = None


def _load_module():
    global _module
    if _module is not None:
        return _module
    fetch_py = settings.project_root / "fetch_eval_record.py"
    if not fetch_py.exists():
        raise FileNotFoundError(
            f"fetch_eval_record.py not found at {fetch_py}. "
            "Expected next to backend/ at project root."
        )
    spec = importlib.util.spec_from_file_location("fetch_eval_record", fetch_py)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module at {fetch_py}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fetch_eval_record"] = mod
    spec.loader.exec_module(mod)
    _module = mod
    return mod


def fetch_one(record_id: str) -> dict:
    """Fetch + parse one record from the iwencai backend.

    Reads IWENCAI_BASE_URL from env; raises if not configured."""
    if not settings.iwencai_base_url:
        raise RuntimeError("IWENCAI_BASE_URL not configured")
    mod = _load_module()
    html = mod.fetch_html(  # type: ignore[attr-defined]
        record_id,
        base_url=settings.iwencai_base_url,
        timeout=30,
        insecure=not settings.iwencai_verify_ssl,
    )
    return mod.parse_record(html)  # type: ignore[attr-defined]


def fetch_many(record_ids: List[str]) -> Tuple[List[dict], List[Tuple[str, str]]]:
    ok: list[dict] = []
    fail: list[tuple[str, str]] = []
    for rid in record_ids:
        try:
            ok.append(fetch_one(rid))
        except Exception as exc:  # noqa: BLE001
            log.warning("iwencai fetch failed for %s: %s", rid, exc)
            fail.append((rid, str(exc)))
    return ok, fail
