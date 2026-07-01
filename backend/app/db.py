"""SQLAlchemy engine + session factory.

SQLite is used in default; can be swapped to Postgres via DB_PATH=postgresql://...
in env without code change.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


def _build_url() -> str:
    raw = settings.db_path
    if raw.startswith(("postgresql", "mysql", "sqlite:")):
        return raw
    # ensure parent dir exists for sqlite
    p = settings.db_path_abs
    p.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{p}"


DATABASE_URL = _build_url()


engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


# Enable foreign keys + WAL for SQLite
@event.listens_for(engine, "connect")
def _sqlite_pragma(dbapi_conn, connection_record):  # noqa: ARG001
    if not DATABASE_URL.startswith("sqlite"):
        return
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("PRAGMA journal_mode = WAL")
    cur.execute("PRAGMA synchronous = NORMAL")
    cur.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    """FastAPI dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session() -> Iterator[Session]:
    """Standalone usage for background tasks."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Create tables if not exist. Runs on every boot; safe + idempotent."""
    from . import models  # noqa: F401 ensure models imported

    Base.metadata.create_all(bind=engine)
    _run_inline_migrations()


def _run_inline_migrations() -> None:
    """Lightweight in-place schema migrations for SQLite.

    Each migration is idempotent: it checks the current state of the DB
    and only runs if needed. Add new entries to MIGRATIONS below; never
    modify a deployed migration once it's been released.
    """
    if not DATABASE_URL.startswith("sqlite"):
        return  # migrations are SQLite-specific for now

    MIGRATIONS = [
        # (description, predicate_sql, action_sql)
        # Predicate should return 1+ rows if migration is NEEDED, else 0 rows.
        # ``action_sql`` may be a single SQL string or a list of strings
        # (executed in order, one execute() per entry — sqlite3 forbids
        # multiple statements per cursor.execute).
        # v1: rename expected_answer → agent_answer on testcases (2026-06-17)
        (
            "rename testcases.expected_answer → agent_answer",
            "SELECT 1 FROM pragma_table_info('testcases') WHERE name='expected_answer'",
            "ALTER TABLE testcases RENAME COLUMN expected_answer TO agent_answer",
        ),
        # v2: add is_custom to test_categories to distinguish user-defined
        # business categories from the 13 seeded self-eval ones (2026-07-01).
        # Predicate returns 1 row when the column is MISSING — i.e. the
        # migration is still needed (inverse of the v1 "rename if exists"
        # pattern, because v2 must NOT run on schemas that already have the
        # column or it would error on duplicate ADD COLUMN).
        (
            "add test_categories.is_custom",
            """SELECT 1 FROM test_categories
               WHERE NOT EXISTS (
                   SELECT 1 FROM pragma_table_info('test_categories')
                   WHERE name='is_custom'
               )""",
            "ALTER TABLE test_categories ADD COLUMN is_custom BOOLEAN DEFAULT 0 NOT NULL",
        ),
        # NOTE on column widths:
        # The TestCategory.code PK + TestCase.category_code FK were widened
        # from String(8) to String(64) in models.py to fit user-defined codes
        # like "批次v1". No DDL migration is required because SQLite uses type
        # affinity and does not enforce VARCHAR(n) length — existing rows
        # accept arbitrary-length strings today, and SQLAlchemy will declare
        # the wider type on the next create_all() (e.g. fresh dev DB).
    ]

    with engine.begin() as conn:
        from sqlalchemy import text
        for desc, pred_sql, action_sql in MIGRATIONS:
            try:
                needed = conn.execute(text(pred_sql)).fetchone()
            except Exception as exc:  # pragma: no cover — table doesn't exist yet
                # First boot before create_all? No — Base.metadata.create_all runs
                # before this. If we hit this, the migration SQL itself is buggy.
                import logging
                logging.getLogger(__name__).warning(
                    "migration predicate failed (skipping %s): %s", desc, exc,
                )
                continue
            if not needed:
                continue
            try:
                statements = action_sql if isinstance(action_sql, list) else [action_sql]
                for stmt in statements:
                    conn.execute(text(stmt))
                import logging
                logging.getLogger(__name__).info("✅ migration applied: %s", desc)
            except Exception as exc:  # pragma: no cover
                import logging
                logging.getLogger(__name__).exception(
                    "migration FAILED (%s): %s", desc, exc,
                )
