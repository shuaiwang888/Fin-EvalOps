"""Tests for the expected_answer → agent_answer rename + DB migration.

Verifies:
- `_normalize_raw` reads both new English key and legacy Chinese key
- The TestCase ORM column is named agent_answer
- The migration logic renames a pre-existing `expected_answer` column
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text


def test_normalize_chinese_key_still_works():
    """Legacy 测试数据 JSON with Chinese keys should still load correctly."""
    from app.routers.testsets import _normalize_raw

    raw = {
        "问题": "纳微科技昨天收盘到今天的情况?",
        "答案": "纳微科技5月13日收盘价...",
        "链路数据": [{"step": 1}],
        "上下文": [{"role": "user"}],
    }
    out = _normalize_raw(raw)
    assert out["question"] == "纳微科技昨天收盘到今天的情况?"
    assert out["agent_answer"] == "纳微科技5月13日收盘价..."
    assert out["reasoning_trace"] == [{"step": 1}]
    assert out["context_history"] == [{"role": "user"}]


def test_normalize_new_english_key():
    """New JSON files using agent_answer key should work too."""
    from app.routers.testsets import _normalize_raw

    raw = {
        "question": "test question",
        "agent_answer": "model's answer here",
        "reasoning_trace": [{"step": 1}],
        "context_history": None,
    }
    out = _normalize_raw(raw)
    assert out["question"] == "test question"
    assert out["agent_answer"] == "model's answer here"


def test_normalize_prefers_new_key_over_legacy():
    """If both keys present, new English key wins."""
    from app.routers.testsets import _normalize_raw

    raw = {
        "问题": "q",
        "答案": "old answer",
        "agent_answer": "new answer",
    }
    out = _normalize_raw(raw)
    assert out["agent_answer"] == "new answer"


def test_testcase_column_renamed():
    """ORM model must have agent_answer, not expected_answer."""
    from app.models import TestCase
    cols = {c.name for c in TestCase.__table__.columns}
    assert "agent_answer" in cols, "TestCase should have agent_answer column"
    assert "expected_answer" not in cols, "TestCase should NOT have expected_answer"


def test_migration_renames_legacy_column():
    """Simulate a pre-rename DB and verify migration renames the column."""
    # Use a temp file-backed sqlite so we control the schema
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        eng = create_engine(f"sqlite:///{db_path}", future=True)

        # 1. Create old-schema table with expected_answer
        with eng.begin() as conn:
            conn.execute(text("""
                CREATE TABLE testcases (
                    id TEXT PRIMARY KEY,
                    source_id TEXT,
                    question TEXT,
                    expected_answer TEXT,
                    category_code TEXT
                )
            """))
            conn.execute(text(
                "INSERT INTO testcases VALUES ('t1','s1','q?','old model answer here','12')"
            ))

        # 2. Run the migration (re-import here to use the temp engine's view)
        from app import db as db_module
        # Monkey-patch DATABASE_URL temporarily for this test
        original_url = db_module.DATABASE_URL
        db_module.DATABASE_URL = f"sqlite:///{db_path}"
        db_module.engine.dispose()
        # Replace engine reference so _run_inline_migrations uses our temp DB
        db_module.engine = eng
        try:
            db_module._run_inline_migrations()
        finally:
            db_module.DATABASE_URL = original_url

        # 3. Verify column was renamed AND data preserved
        with eng.connect() as conn:
            cols = {row[1] for row in conn.execute(text("PRAGMA table_info(testcases)"))}
            assert "agent_answer" in cols
            assert "expected_answer" not in cols

            value = conn.execute(text(
                "SELECT agent_answer FROM testcases WHERE id='t1'"
            )).scalar()
            assert value == "old model answer here"

        # 4. Running again should be a no-op (idempotent)
        db_module.engine = eng
        db_module._run_inline_migrations()
        with eng.connect() as conn:
            value = conn.execute(text(
                "SELECT agent_answer FROM testcases WHERE id='t1'"
            )).scalar()
            assert value == "old model answer here"
    finally:
        Path(db_path).unlink(missing_ok=True)
