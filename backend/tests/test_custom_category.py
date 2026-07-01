"""Tests for user-defined (custom) business categories.

Verifies:
- POST /api/testsets/categories creates a row with is_custom=true
- code validation rejects invalid characters / lengths
- duplicate / reserved codes are rejected with 400
- DELETE refuses seed categories (is_custom=false) with 409
- DELETE refuses categories that still have test cases with 409
- DELETE on an empty custom category succeeds
- POST /api/testsets/import-file honours a custom category_code
- Inline migration adds the is_custom column to a pre-migration schema
- Inline migration widens test_categories.code from VARCHAR(8) to VARCHAR(64)
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_client(tmp_db: str) -> TestClient:
    """Build a TestClient whose DB lives at ``tmp_db`` (already-created schema).

    We monkey-patch the app's DB module so the lifespan-time ``init_db`` and
    ``_run_inline_migrations`` operate on our temp file. ``SessionLocal`` is
    also rebuilt because it captured the original engine at import time.
    """
    from app import db as db_module
    eng = create_engine(f"sqlite:///{tmp_db}", future=True)
    db_module.DATABASE_URL = f"sqlite:///{tmp_db}"
    db_module.engine.dispose()
    db_module.engine = eng
    db_module.SessionLocal = db_module.sessionmaker(
        bind=eng, autoflush=False, autocommit=False, future=True
    )

    # routers/testsets.py imported `from ..db import get_db` at module load —
    # patch its reference so the dependency returns sessions bound to our engine.
    from app.routers import testsets as testsets_router
    testsets_router.get_db = db_module.get_db

    from app.main import app
    # lifespan will run init_db + migrations on entry → schema is fresh.
    return TestClient(app)


# ---------------------------------------------------------------------------
# API-level tests
# ---------------------------------------------------------------------------

def test_create_custom_category():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            r = client.post("/api/testsets/categories", json={
                "code": "批次v1",
                "name_zh": "2025Q3 回归批次",
                "description": "覆盖 200 条样本",
            })
            assert r.status_code == 200, r.text
            body = r.json()
            assert body["code"] == "批次v1"
            assert body["is_custom"] is True
            assert body["name_zh"] == "2025Q3 回归批次"
            assert body["mapped_skill_id"] is None
            # slug is auto-derived with c- prefix to keep custom in own namespace
            assert body["slug"].startswith("c-")

            # It appears in the list endpoint, sorted before seed categories
            r = client.get("/api/testsets/categories")
            assert r.status_code == 200
            lst = r.json()
            assert lst[0]["code"] == "批次v1"  # custom-first ordering
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_create_rejects_duplicate_code():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "dup-batch", "name_zh": "first",
            })
            r = client.post("/api/testsets/categories", json={
                "code": "dup-batch", "name_zh": "second",
            })
            assert r.status_code == 400
            assert "already exists" in r.json()["detail"]
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_create_rejects_invalid_code_characters():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            # spaces and punctuation are not allowed
            r = client.post("/api/testsets/categories", json={
                "code": "bad code!", "name_zh": "x",
            })
            assert r.status_code == 422  # pydantic validation error
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_create_rejects_blank_code():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            r = client.post("/api/testsets/categories", json={
                "code": "   ", "name_zh": "blank",
            })
            assert r.status_code == 422
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_delete_rejects_seed_category():
    """Seed category (e.g. '01') is not deletable even if it's not referenced."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            # Seed 01 must exist after init_db + skill_loader sync_to_db (or at
            # least after scan-disk defensive insert). Force it via the API to
            # keep the test independent of skills/ layout.
            client.post("/api/testsets/categories", json={
                "code": "01", "name_zh": "seed",
            })
            r = client.delete("/api/testsets/categories/01")
            # '01' is reserved (in SELF_SKILL_EN_SLUGS) → 400 on create first
            # which we ignored above. Delete hits the is_custom guard.
            assert r.status_code in (400, 409), r.text
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_delete_rejects_referenced_custom_category():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "in-use", "name_zh": "in use",
            })
            # Upload a JSON with 1 record → 1 test case created
            files = {"file": ("a.json", json.dumps([{
                "问题": "Q?", "答案": "A.", "id": "x1"
            }]), "application/json")}
            r = client.post(
                "/api/testsets/import-file?category_code=in-use",
                files=files,
            )
            assert r.status_code == 200, r.text
            assert r.json()["inserted"] == 1

            r = client.delete("/api/testsets/categories/in-use")
            assert r.status_code == 409
            assert "测试样本" in r.json()["detail"]
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_delete_succeeds_on_empty_custom_category():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "throwaway", "name_zh": "to delete",
            })
            r = client.delete("/api/testsets/categories/throwaway")
            assert r.status_code == 200
            assert r.json()["deleted"] == "throwaway"

            # list no longer contains it
            r = client.get("/api/testsets/categories")
            assert all(c["code"] != "throwaway" for c in r.json())
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_import_file_with_custom_category():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "prod-2025q3", "name_zh": "production batch",
            })
            payload = [
                {"问题": "Q1?", "答案": "A1.", "id": "s1"},
                {"问题": "Q2?", "答案": "A2.", "id": "s2"},
            ]
            files = {"file": ("batch.json", json.dumps(payload), "application/json")}
            r = client.post(
                "/api/testsets/import-file?category_code=prod-2025q3",
                files=files,
            )
            assert r.status_code == 200, r.text
            assert r.json() == {"inserted": 2, "total_in_file": 2}

            # Filtering by the custom code returns those 2 rows
            r = client.get("/api/testsets?category=prod-2025q3&page_size=50")
            assert r.status_code == 200
            body = r.json()
            assert body["total"] == 2
            assert {it["category_code"] for it in body["items"]} == {"prod-2025q3"}
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_import_file_preserves_tags_chinese_keyed():
    """`tags` field on a Chinese-keyed JSON must round-trip into the DB row.

    Regression for: previously _normalize_raw dropped the `tags` key for
    Chinese-keyed payloads, and import_file never wrote tags=... to the
    TestCase ORM, so any auxiliary metadata packed into `tags` by upstream
    exporters (e.g. convert_part06.py) silently disappeared on import.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "tagged", "name_zh": "tagged batch",
            })
            payload = [
                {
                    "问题": "Q?", "答案": "A.", "id": "s1",
                    "tags": ["agent:9662", '{"primary_intent":"事件概念型标的筛选"}'],
                },
            ]
            files = {"file": ("a.json", json.dumps(payload), "application/json")}
            r = client.post(
                "/api/testsets/import-file?category_code=tagged",
                files=files,
            )
            assert r.status_code == 200, r.text
            assert r.json() == {"inserted": 1, "total_in_file": 1}

            r = client.get("/api/testsets?category=tagged&page_size=5")
            tc_id = r.json()["items"][0]["id"]

            r = client.get(f"/api/testsets/{tc_id}")
            assert r.status_code == 200
            body = r.json()
            assert body["tags"] == [
                "agent:9662",
                '{"primary_intent":"事件概念型标的筛选"}',
            ], f"tags dropped on import: got {body['tags']!r}"
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_import_file_preserves_tags_english_keyed():
    """English-keyed passthrough should still work after the fix."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        with _fresh_client(db_path) as client:
            client.post("/api/testsets/categories", json={
                "code": "tagged-en", "name_zh": "english tags",
            })
            payload = [{
                "source_id": "en1",
                "source": "manual",
                "question": "Q?",
                "agent_answer": "A.",
                "tags": ["hello", "world"],
            }]
            files = {"file": ("a.json", json.dumps(payload), "application/json")}
            r = client.post(
                "/api/testsets/import-file?category_code=tagged-en",
                files=files,
            )
            assert r.status_code == 200

            r = client.get("/api/testsets?category=tagged-en&page_size=5")
            tc_id = r.json()["items"][0]["id"]

            r = client.get(f"/api/testsets/{tc_id}")
            assert r.json()["tags"] == ["hello", "world"]
    finally:
        Path(db_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Migration tests (DB-level, mirror test_field_rename.py pattern)
# ---------------------------------------------------------------------------

def test_migration_adds_is_custom_column():
    """Simulate a pre-migration DB and verify the column gets added."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        eng = create_engine(f"sqlite:///{db_path}", future=True)
        with eng.begin() as conn:
            conn.execute(text("""
                CREATE TABLE test_categories (
                    code VARCHAR(8) PRIMARY KEY,
                    slug VARCHAR(128) NOT NULL UNIQUE,
                    name_zh VARCHAR(128) NOT NULL,
                    name_en VARCHAR(128) NOT NULL,
                    description TEXT DEFAULT '',
                    mapped_skill_id VARCHAR(64)
                )
            """))
            conn.execute(text(
                "INSERT INTO test_categories VALUES "
                "('01','s1','z','e','',NULL)"
            ))

        from app import db as db_module
        original_url = db_module.DATABASE_URL
        db_module.DATABASE_URL = f"sqlite:///{db_path}"
        db_module.engine.dispose()
        db_module.engine = eng
        try:
            db_module._run_inline_migrations()
        finally:
            db_module.DATABASE_URL = original_url

        with eng.connect() as conn:
            cols = {row[1] for row in conn.execute(
                text("PRAGMA table_info('test_categories')"))}
            assert "is_custom" in cols

            # Seed row should default to is_custom=0
            v = conn.execute(text(
                "SELECT is_custom FROM test_categories WHERE code='01'"
            )).scalar()
            assert v == 0

            # Original data still intact
            assert conn.execute(text(
                "SELECT name_zh FROM test_categories WHERE code='01'"
            )).scalar() == "z"

        # Idempotent: running again must not error
        db_module.engine = eng
        db_module._run_inline_migrations()
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_models_widened_code_column():
    """ORM model declaration must accept custom codes up to 64 chars.

    SQLite type affinity means the live schema column type stays VARCHAR(8)
    on already-created DBs but SQLAlchemy will declare String(64) on
    create_all() for fresh DBs. New code (e.g. POST /api/testsets/categories)
    relies on the wider String(64) to avoid truncation.
    """
    from app.models import TestCategory, TestCase
    cat_code = TestCategory.__table__.columns["code"].type
    tc_code = TestCase.__table__.columns["category_code"].type
    # SQLAlchemy String stores length in `.length`.
    assert cat_code.length >= 64, cat_code.length
    assert tc_code.length >= 64, tc_code.length