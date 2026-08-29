"""Regression coverage for cross-layer routing and data-integrity defects."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine


def _fresh_client(tmp_db: str) -> TestClient:
    os.environ.setdefault("MINIMAX_API_KEY", "sk-fake-for-tests-only")
    from app import db as db_module

    eng = create_engine(f"sqlite:///{tmp_db}", future=True)
    db_module.DATABASE_URL = f"sqlite:///{tmp_db}"
    db_module.engine.dispose()
    db_module.engine = eng
    db_module.SessionLocal = db_module.sessionmaker(
        bind=eng, autoflush=False, autocommit=False, future=True
    )
    from app.main import app

    return TestClient(app)


def test_static_batch_list_route_is_not_swallowed_by_run_detail():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            response = client.get("/api/runs/batches")
            assert response.status_code == 200, response.text
            assert response.json() == []
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_deleting_a_run_cascades_its_annotations():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            from app.db import db_session
            from app.models import Annotation, Run, Skill, TestCase, TestCategory

            with db_session() as db:
                db.add(TestCategory(
                    code="x", slug="x", name_zh="x", name_en="x", is_custom=True
                ))
                db.add(Skill(
                    id="self/x", family="self", code="x", name_zh="x",
                    name_en="x", schema_version="v1", path="/tmp/x",
                ))
                tc = TestCase(
                    id="tc-x", source_id="src-x", category_code="x",
                    question="Q", agent_answer="A",
                )
                run = Run(
                    id="run-x", testcase_id="tc-x", skill_id="self/x",
                    judge_model="minimax-3", judge_provider="minimax",
                    status="done", progress_pct=100,
                )
                db.add_all([tc, run, Annotation(id="ann-x", run_id="run-x")])

            response = client.delete("/api/runs/run-x")
            assert response.status_code == 200, response.text
            with db_session() as db:
                assert db.get(Annotation, "ann-x") is None
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_explicit_unconfigured_model_never_silently_falls_back(monkeypatch):
    from app.services.llm_client import resolve_model

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-fake-for-tests-only")
    try:
        resolve_model("gpt-4o")
    except RuntimeError as exc:
        assert "gpt-4o" in str(exc)
    else:  # pragma: no cover - documents the integrity guarantee
        raise AssertionError("explicit model unexpectedly fell back")
