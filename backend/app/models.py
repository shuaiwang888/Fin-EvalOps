"""SQLAlchemy ORM models — see plan §3 数据模型 for design rationale."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return uuid.uuid4().hex


# ---------------------- Skill catalog (parsed from filesystem) ----------------------
class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # e.g. "self/03"
    family: Mapped[str] = mapped_column(String(16), index=True)  # self | competitor | e2e
    code: Mapped[str] = mapped_column(String(8), index=True)  # 01..14
    name_zh: Mapped[str] = mapped_column(String(128))
    name_en: Mapped[str] = mapped_column(String(128))
    schema_version: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text, default="")
    one_liner: Mapped[str] = mapped_column(String(256), default="")
    path: Mapped[str] = mapped_column(Text)
    dimensions: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    caps: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    root_causes: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    tools: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    golden_case_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)


# ---------------------- Test categories (seeded 01..13 + user-defined custom) ------
class TestCategory(Base):
    __tablename__ = "test_categories"

    # Seeded categories use short codes like "01"..13"; user-created custom
    # categories may use longer semantic codes (e.g. "批次v1", "batch-2025q3").
    # 64 chars fits both comfortably and is the upper bound enforced by the
    # POST /api/testsets/categories validator.
    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True)
    name_zh: Mapped[str] = mapped_column(String(128))
    name_en: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text, default="")
    mapped_skill_id: Mapped[Optional[str]] = mapped_column(String(64), default=None)
    # True for user-defined categories (created via POST /api/testsets/categories).
    # Seeded categories from skill_loader / scan_disk stay False and cannot be deleted.
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    testcases: Mapped[list["TestCase"]] = relationship(back_populates="category")


# ---------------------- TestCases (rows) ----------------------
class TestCase(Base):
    __tablename__ = "testcases"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    source_id: Mapped[str] = mapped_column(String(64), index=True)  # ans_xxx
    # FK width must match TestCategory.code (String(64)) — widened from 8 to allow
    # custom category codes longer than 2 digits.
    category_code: Mapped[str] = mapped_column(
        String(64), ForeignKey("test_categories.code"), index=True
    )
    file_path: Mapped[Optional[str]] = mapped_column(Text, default=None)
    source: Mapped[str] = mapped_column(String(32), default="iwencai")

    question: Mapped[str] = mapped_column(Text)
    agent_answer: Mapped[str] = mapped_column(Text)
    reasoning_trace: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    context_history: Mapped[Optional[list]] = mapped_column(JSON, default=None)

    language: Mapped[str] = mapped_column(String(16), default="zh")  # zh | en | mixed
    has_charts: Mapped[bool] = mapped_column(Boolean, default=False)
    tool_set: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    inferred_difficulty: Mapped[str] = mapped_column(String(16), default="medium")
    tags: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    imported_from: Mapped[str] = mapped_column(String(16), default="file")  # file|fetch|manual

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    category: Mapped[TestCategory] = relationship(back_populates="testcases")
    runs: Mapped[list["Run"]] = relationship(back_populates="testcase", cascade="all, delete-orphan")


Index("ix_testcases_category_lang", TestCase.category_code, TestCase.language)


# ---------------------- Run batches ----------------------
class RunBatch(Base):
    __tablename__ = "run_batches"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    label: Mapped[str] = mapped_column(String(256), default="")
    judge_model: Mapped[str] = mapped_column(String(64))
    judge_provider: Mapped[str] = mapped_column(String(32))
    total: Mapped[int] = mapped_column(Integer, default=0)
    done: Mapped[int] = mapped_column(Integer, default=0)
    failed: Mapped[int] = mapped_column(Integer, default=0)
    skill_strategy: Mapped[str] = mapped_column(String(16), default="auto")  # auto|manual
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, index=True)

    runs: Mapped[list["Run"]] = relationship(back_populates="batch")


# ---------------------- Runs ----------------------
class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    batch_id: Mapped[Optional[str]] = mapped_column(
        String(64), ForeignKey("run_batches.id"), default=None, index=True
    )
    testcase_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("testcases.id"), index=True
    )
    skill_id: Mapped[str] = mapped_column(String(64), ForeignKey("skills.id"), index=True)

    judge_model: Mapped[str] = mapped_column(String(64), index=True)
    judge_provider: Mapped[str] = mapped_column(String(32))

    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    # pending | routing | running | scoring | done | failed | cancelled
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)
    current_step: Mapped[str] = mapped_column(String(32), default="")

    routing: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    raw_response: Mapped[Optional[dict]] = mapped_column(JSON, default=None)

    weight_assignment: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    dimension_scores: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    caps: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    root_causes: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    narrative_review: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    matched_golden_cases: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    skipped_dimensions: Mapped[Optional[list]] = mapped_column(JSON, default=None)

    absolute_score_pre_cap: Mapped[Optional[float]] = mapped_column(Float, default=None)
    final_score: Mapped[Optional[float]] = mapped_column(Float, default=None, index=True)

    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    tokens_in: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    tokens_out: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    cost_usd: Mapped[Optional[float]] = mapped_column(Float, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, index=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)
    error_msg: Mapped[Optional[str]] = mapped_column(Text, default=None)

    testcase: Mapped[TestCase] = relationship(back_populates="runs")
    batch: Mapped[Optional[RunBatch]] = relationship(back_populates="runs")


Index("ix_runs_skill_model_created", Run.skill_id, Run.judge_model, Run.created_at)


# ---------------------- Annotations (P1) ----------------------
class Annotation(Base):
    __tablename__ = "annotations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    run_id: Mapped[str] = mapped_column(String(64), ForeignKey("runs.id"), index=True)
    reviewer: Mapped[str] = mapped_column(String(64), default="anonymous")
    dim_overrides: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    comment: Mapped[str] = mapped_column(Text, default="")
    is_golden: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


# ---------------------- Data Agent chat history ----------------------
class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(256), default="New conversation")
    model: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    messages: Mapped[list["AgentMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="AgentMessage.created_at"
    )


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("agent_sessions.id"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))  # user | assistant | tool
    content: Mapped[str] = mapped_column(Text, default="")
    sql_used: Mapped[Optional[str]] = mapped_column(Text, default=None)
    chart_spec: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    data_preview: Mapped[Optional[list]] = mapped_column(JSON, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    session: Mapped[AgentSession] = relationship(back_populates="messages")
