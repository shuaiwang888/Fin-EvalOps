"""Pydantic schemas for request/response bodies.

Models are kept thin and re-use ORM dict shapes wherever possible. Internal
JSON blobs (dimensions, caps, root_causes, raw_response) are passed through as
opaque `Any` since their schema differs per Skill version.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------- Common ----------------------
class _OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------------------- Skill ----------------------
class SkillBrief(_OrmBase):
    id: str
    family: str
    code: str
    name_zh: str
    name_en: str
    schema_version: str
    one_liner: str = ""
    golden_case_count: int = 0


class SkillDetail(SkillBrief):
    description: str = ""
    path: str
    dimensions: Optional[Any] = None
    caps: Optional[Any] = None
    root_causes: Optional[Any] = None
    tools: Optional[Any] = None
    updated_at: datetime


# ---------------------- TestCategory ----------------------
class TestCategoryOut(_OrmBase):
    code: str
    slug: str
    name_zh: str
    name_en: str
    description: str = ""
    mapped_skill_id: Optional[str] = None


# ---------------------- TestCase ----------------------
class TestCaseBrief(_OrmBase):
    id: str
    source_id: str
    category_code: str
    question: str
    language: str
    has_charts: bool
    inferred_difficulty: str
    tags: Optional[List[str]] = None
    imported_from: str
    created_at: datetime


class TestCaseDetail(TestCaseBrief):
    source: str
    expected_answer: str
    reasoning_trace: Optional[List[Any]] = None
    context_history: Optional[List[Any]] = None
    tool_set: Optional[List[str]] = None
    file_path: Optional[str] = None
    updated_at: datetime


class TestCaseCreate(BaseModel):
    """Either provide raw JSON identical to dataset format, or fields."""
    category_code: str
    source_id: Optional[str] = None
    source: str = "iwencai"
    question: str
    expected_answer: str
    reasoning_trace: Optional[List[Any]] = None
    context_history: Optional[List[Any]] = None
    tags: Optional[List[str]] = None
    file_path: Optional[str] = None


class TestCaseUpdate(BaseModel):
    question: Optional[str] = None
    expected_answer: Optional[str] = None
    reasoning_trace: Optional[List[Any]] = None
    context_history: Optional[List[Any]] = None
    tags: Optional[List[str]] = None


class TestCaseImportRaw(BaseModel):
    """Raw json from 数据测试集 — Chinese keys."""
    raw: Any
    category_code: str
    file_path: Optional[str] = None


class IwencaiImportRequest(BaseModel):
    record_ids: List[str] = Field(default_factory=list, max_length=200)
    category_code: str


class IwencaiImportResponse(BaseModel):
    imported: int
    failed: List[dict]


class ScanDiskResponse(BaseModel):
    scanned: int
    inserted: int
    updated: int
    skipped: int


# ---------------------- Routing ----------------------
class RouteRequest(BaseModel):
    question: str
    context: Optional[List[dict]] = None
    hint_skill: Optional[str] = None
    judge_model: Optional[str] = None


class RouteAlternative(BaseModel):
    skill: str
    skill_id: str
    why: str


class RouteResponse(BaseModel):
    predicted_skill: str
    skill_id: str
    confidence: float
    reasoning: str
    alternatives: List[RouteAlternative] = []
    stage_used: Literal["keyword", "llm", "fallback", "hint"] = "llm"
    fallback: bool = False


# ---------------------- Run ----------------------
class RunCreate(BaseModel):
    testcase_id: str
    skill_id: Optional[str] = None  # if None → auto-route
    judge_model: Optional[str] = None
    note: Optional[str] = None


class RunBatchCreate(BaseModel):
    testcase_ids: List[str] = Field(min_length=1, max_length=500)
    skill_strategy: Literal["auto", "manual"] = "auto"
    skill_id: Optional[str] = None  # required when strategy == manual
    judge_model: Optional[str] = None
    label: Optional[str] = None


class RunBrief(_OrmBase):
    id: str
    batch_id: Optional[str] = None
    testcase_id: str
    skill_id: str
    judge_model: str
    judge_provider: str
    status: str
    progress_pct: int
    current_step: str = ""
    final_score: Optional[float] = None
    absolute_score_pre_cap: Optional[float] = None
    latency_ms: Optional[int] = None
    tokens_in: Optional[int] = None
    tokens_out: Optional[int] = None
    created_at: datetime
    finished_at: Optional[datetime] = None
    error_msg: Optional[str] = None


class RunDetail(RunBrief):
    routing: Optional[Any] = None
    raw_response: Optional[Any] = None
    weight_assignment: Optional[Any] = None
    dimension_scores: Optional[Any] = None
    caps: Optional[Any] = None
    root_causes: Optional[Any] = None
    narrative_review: Optional[Any] = None
    matched_golden_cases: Optional[Any] = None
    skipped_dimensions: Optional[Any] = None


class RunBatchOut(_OrmBase):
    id: str
    label: str
    judge_model: str
    judge_provider: str
    total: int
    done: int
    failed: int
    skill_strategy: str
    created_at: datetime


# ---------------------- Dashboard ----------------------
class DashboardSummary(BaseModel):
    total_testcases: int
    total_runs: int
    avg_score: Optional[float]
    pass_rate: Optional[float]
    by_skill: List[dict]
    by_l1_root_cause: List[dict]
    available_models: List[str]
    available_providers: List[str]
    last_24h_runs: int


class DashboardTrendPoint(BaseModel):
    date: str
    skill_id: Optional[str] = None
    avg_score: float
    count: int


class TopFailureRow(BaseModel):
    run_id: str
    testcase_id: str
    question_preview: str
    skill_id: str
    final_score: float
    caps_triggered: List[str]
    top_root_cause: Optional[str] = None
    created_at: datetime


# ---------------------- Data Agent ----------------------
class AgentMessageIn(BaseModel):
    content: str
    model: Optional[str] = None


class AgentMessageOut(_OrmBase):
    id: str
    session_id: str
    role: str
    content: str
    sql_used: Optional[str] = None
    chart_spec: Optional[Any] = None
    data_preview: Optional[Any] = None
    created_at: datetime


class AgentSessionBrief(_OrmBase):
    id: str
    title: str
    model: str
    created_at: datetime
    updated_at: datetime


class AgentSessionDetail(AgentSessionBrief):
    messages: List[AgentMessageOut] = []


# ---------------------- Annotation ----------------------
class AnnotationCreate(BaseModel):
    run_id: str
    reviewer: str = "anonymous"
    dim_overrides: Optional[dict] = None
    comment: str = ""
    is_golden: bool = False


class AnnotationOut(_OrmBase):
    id: str
    run_id: str
    reviewer: str
    dim_overrides: Optional[Any] = None
    comment: str
    is_golden: bool
    created_at: datetime


# ---------------------- Misc ----------------------
class ReloadSkillsResponse(BaseModel):
    self: int
    competitor: int
    e2e: int
    total: int


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    providers: List[str]
    db: str
