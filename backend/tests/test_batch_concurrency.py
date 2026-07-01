"""Tests for batch evaluation features.

Covers:
- DELETE /api/runs/{run_id} (single + refuses in-flight)
- POST /api/runs/delete-batch (bulk; returns deleted / skipped_busy / skipped_missing)
- list_runs includes testcase_question from JOIN
- eval_batch_concurrency setting + sane default
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_client(tmp_db: str) -> TestClient:
    """Spin up a TestClient whose DB lives at tmp_db (schema built fresh).

    Also seeds a dummy MINIMAX_API_KEY so /api/runs can resolve a
    default judge model — the actual LLM call never runs in these tests
    because we mark the Run status as 'done' directly in the DB before
    exercising delete endpoints.
    """
    import os
    os.environ.setdefault("MINIMAX_API_KEY", "sk-fake-for-tests-only")

    from app import db as db_module
    from sqlalchemy import create_engine as _ce
    eng = _ce(f"sqlite:///{tmp_db}", future=True)
    db_module.DATABASE_URL = f"sqlite:///{tmp_db}"
    db_module.engine.dispose()
    db_module.engine = eng
    db_module.SessionLocal = db_module.sessionmaker(
        bind=eng, autoflush=False, autocommit=False, future=True
    )
    from app.routers import testsets as testsets_router
    testsets_router.get_db = db_module.get_db

    from app.main import app
    return TestClient(app)


def _seed_one_testcase(client: TestClient, code: str = "t1") -> str:
    """Create a custom category + a single test case via the API."""
    client.post("/api/testsets/categories", json={"code": code, "name_zh": code})
    payload = [{"id": "src-1", "问题": "Q?", "答案": "A."}]
    files = {"file": ("a.json", __import__("json").dumps(payload), "application/json")}
    r = client.post(f"/api/testsets/import-file?category_code={code}", files=files)
    assert r.status_code == 200, r.text
    r = client.get(f"/api/testsets?category={code}&page_size=5")
    return r.json()["items"][0]["id"]


# ---------------------------------------------------------------------------
# DELETE single
# ---------------------------------------------------------------------------

def test_delete_run_does_not_exist_returns_404():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            r = client.delete("/api/runs/does-not-exist")
            assert r.status_code == 404
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_delete_done_run_succeeds():
    """A finished (done/failed/cancelled) Run can be deleted; 200 + deleted id."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            tc_id = _seed_one_testcase(client)
            r = client.post(
                "/api/runs",
                json={"testcase_id": tc_id, "judge_model": "minimax-3"},
            )
            assert r.status_code == 201, r.text
            run_id = r.json()["id"]

            # Simulate the run finishing by directly updating status.
            # The actual run is queued; we don't want to wait for the LLM.
            from app.db import db_session
            from app.models import Run
            from datetime import datetime, timezone
            with db_session() as db:
                run = db.get(Run, run_id)
                run.status = "done"
                run.finished_at = datetime.now(timezone.utc)

            r = client.delete(f"/api/runs/{run_id}")
            assert r.status_code == 200, r.text
            assert r.json() == {"deleted": run_id}

            # And it's actually gone from the DB
            r = client.get(f"/api/runs/{run_id}")
            assert r.status_code == 404
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_delete_in_flight_run_returns_409():
    """In-flight Runs (pending/routing/running/scoring) must not be deletable.

    We insert the Run row directly to avoid actually starting the evaluator
    background task — we just want to test the DELETE endpoint's status check.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            tc_id = _seed_one_testcase(client)
            # Insert directly, bypassing /api/runs (which would start the
            # background eval task that would transition status to 'failed').
            from app.db import db_session
            from app.models import Run
            from app.services.llm_client import resolve_model
            spec = resolve_model("minimax-3")
            run_id = "in-flight-test-id"
            with db_session() as db:
                db.add(Run(
                    id=run_id,
                    testcase_id=tc_id,
                    skill_id="self/01",
                    judge_model=spec.id,
                    judge_provider=spec.provider,
                    status="running",
                    progress_pct=50,
                    current_step="step1",
                ))

            r = client.delete(f"/api/runs/{run_id}")
            assert r.status_code == 409, r.text
            assert "状态" in r.json()["detail"] or "评测中" in r.json()["detail"]
    finally:
        Path(db_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# DELETE batch
# ---------------------------------------------------------------------------

def test_delete_runs_batch_mixed_outcomes():
    """Bulk delete returns 3 lists: deleted, skipped_busy, skipped_missing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            tc_id = _seed_one_testcase(client)
            # Insert two runs directly: one done (deletable), one running (skipped).
            from app.db import db_session
            from app.models import Run
            from app.services.llm_client import resolve_model
            from datetime import datetime, timezone
            spec = resolve_model("minimax-3")
            done_id, busy_id = "batch-done-id", "batch-busy-id"
            with db_session() as db:
                db.add(Run(
                    id=done_id,
                    testcase_id=tc_id,
                    skill_id="self/01",
                    judge_model=spec.id,
                    judge_provider=spec.provider,
                    status="done",
                    progress_pct=100,
                    current_step="done",
                    finished_at=datetime.now(timezone.utc),
                ))
                db.add(Run(
                    id=busy_id,
                    testcase_id=tc_id,
                    skill_id="self/01",
                    judge_model=spec.id,
                    judge_provider=spec.provider,
                    status="running",
                    progress_pct=20,
                    current_step="step1",
                ))

            payload = {"run_ids": [done_id, busy_id, "non-existent"]}
            r = client.post("/api/runs/delete-batch", json=payload)
            assert r.status_code == 200, r.text
            body = r.json()
            assert body["deleted"] == [done_id]
            assert body["skipped_busy"] == [busy_id]
            assert body["skipped_missing"] == ["non-existent"]
    finally:
        Path(db_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# list_runs JOIN — testcase_question surfaces on the row
# ---------------------------------------------------------------------------

def test_list_runs_includes_testcase_question():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            tc_id = _seed_one_testcase(client)
            client.post("/api/runs", json={"testcase_id": tc_id})

            r = client.get("/api/runs")
            assert r.status_code == 200
            assert r.json()["total"] == 1
            item = r.json()["items"][0]
            assert item["testcase_question"] == "Q?"
            assert item["testcase_id"] == tc_id
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_get_run_includes_testcase_question():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            tc_id = _seed_one_testcase(client)
            run_id = client.post("/api/runs", json={"testcase_id": tc_id}).json()["id"]

            r = client.get(f"/api/runs/{run_id}")
            assert r.status_code == 200
            assert r.json()["testcase_question"] == "Q?"
    finally:
        Path(db_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Config: eval_batch_concurrency
# ---------------------------------------------------------------------------

def test_eval_batch_concurrency_default_is_3():
    """The default must be conservative — 3 concurrent jobs is safe for
    most LLM rate limits. If you've changed this, update the docs too."""
    from app.config import settings
    assert settings.eval_batch_concurrency == 3


def test_eval_batch_concurrency_env_override(monkeypatch):
    """Tunable via env var."""
    monkeypatch.setenv("EVAL_BATCH_CONCURRENCY", "5")
    from app import config as cfg
    s = cfg.Settings()
    assert s.eval_batch_concurrency == 5
    monkeypatch.delenv("EVAL_BATCH_CONCURRENCY")