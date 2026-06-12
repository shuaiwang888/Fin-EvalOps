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
