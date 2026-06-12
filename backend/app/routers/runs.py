"""Runs router — create / batch / list / detail / route preview."""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Run, RunBatch, Skill, TestCase
from ..schemas import (
    RouteRequest,
    RouteResponse,
    RunBatchCreate,
    RunBatchOut,
    RunBrief,
    RunCreate,
    RunDetail,
)
from ..services import evaluator, llm_client, skill_router

router = APIRouter()


# ----------------------------------------------------------------------------
# Routing preview (no run created)
# ----------------------------------------------------------------------------
@router.post("/route", response_model=RouteResponse)
def preview_route(body: RouteRequest):
    r = skill_router.route(
        body.question,
        judge_model=body.judge_model,
        hint_skill_id=body.hint_skill,
    )
    return RouteResponse(
        predicted_skill=r.skill_code,
        skill_id=r.skill_id,
        confidence=r.confidence,
        reasoning=r.reasoning,
        alternatives=r.alternatives,
        stage_used=r.stage_used,
        fallback=r.fallback,
    )


# ----------------------------------------------------------------------------
# Models — what the frontend dropdown should show
# ----------------------------------------------------------------------------
@router.get("/models")
def list_models():
    return {"models": llm_client.list_models()}


# ----------------------------------------------------------------------------
# Create single run
# ----------------------------------------------------------------------------
@router.post("/runs", response_model=RunBrief, status_code=201)
def create_run(body: RunCreate, bg: BackgroundTasks, db: Session = Depends(get_db)):
    tc = db.get(TestCase, body.testcase_id)
    if not tc:
        raise HTTPException(404, f"TestCase {body.testcase_id} not found")

    skill_id = body.skill_id
    routing_meta: dict | None = None
    # Only auto-route when the user did not specify a skill_id
    if not skill_id:
        r = skill_router.route(tc.question, judge_model=body.judge_model)
        skill_id = r.skill_id
        routing_meta = {
            "predicted_skill": r.skill_code,
            "skill_id": r.skill_id,
            "confidence": r.confidence,
            "reasoning": r.reasoning,
            "alternatives": r.alternatives,
            "stage_used": r.stage_used,
            "fallback": r.fallback,
        }

    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(400, f"Skill {skill_id} unknown")

    spec = llm_client.resolve_model(body.judge_model)
    run = Run(
        testcase_id=tc.id,
        skill_id=skill.id,
        judge_model=spec.id,
        judge_provider=spec.provider,
        routing=routing_meta,
        status="pending",
        progress_pct=0,
        current_step="queued",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    bg.add_task(evaluator.evaluate_run, run.id)
    return run


# ----------------------------------------------------------------------------
# Batch create
# ----------------------------------------------------------------------------
@router.post("/runs/batch", response_model=RunBatchOut, status_code=201)
def create_batch(body: RunBatchCreate, bg: BackgroundTasks, db: Session = Depends(get_db)):
    if body.skill_strategy == "manual":
        if not body.skill_id:
            raise HTTPException(400, "skill_id required when strategy=manual")
        if not db.get(Skill, body.skill_id):
            raise HTTPException(400, f"Skill {body.skill_id} not found")
    spec = llm_client.resolve_model(body.judge_model)

    batch = RunBatch(
        id=uuid.uuid4().hex,
        label=body.label or "",
        judge_model=spec.id,
        judge_provider=spec.provider,
        total=len(body.testcase_ids),
        skill_strategy=body.skill_strategy,
    )
    db.add(batch)
    db.flush()

    run_ids: list[str] = []
    for tc_id in body.testcase_ids:
        tc = db.get(TestCase, tc_id)
        if not tc:
            continue
        routing_meta = None
        skill_id = body.skill_id
        if body.skill_strategy == "auto":
            r = skill_router.route(tc.question, judge_model=body.judge_model)
            skill_id = r.skill_id
            routing_meta = {
                "predicted_skill": r.skill_code, "skill_id": r.skill_id,
                "confidence": r.confidence, "reasoning": r.reasoning,
                "alternatives": r.alternatives, "stage_used": r.stage_used,
                "fallback": r.fallback,
            }
        run = Run(
            batch_id=batch.id,
            testcase_id=tc.id,
            skill_id=skill_id,
            judge_model=spec.id,
            judge_provider=spec.provider,
            routing=routing_meta,
            status="pending", progress_pct=0, current_step="queued",
        )
        db.add(run)
        db.flush()
        run_ids.append(run.id)
    batch.total = len(run_ids)
    db.commit()
    db.refresh(batch)

    bg.add_task(evaluator.evaluate_batch, batch.id, run_ids)
    return batch


# ----------------------------------------------------------------------------
# List & filter
# ----------------------------------------------------------------------------
# Allow-list of columns that can be used as sort keys, mapped to ORM column
# objects. Prevents arbitrary `?sort=` injection.
_SORT_COLUMNS = {
    "created_at": Run.created_at,
    "finished_at": Run.finished_at,
    "final_score": Run.final_score,
    "latency_ms": Run.latency_ms,
    "tokens_in": Run.tokens_in,
    "status": Run.status,
    "skill_id": Run.skill_id,
    "judge_model": Run.judge_model,
}


@router.get("/runs", response_model=dict)
def list_runs(
    status: Optional[str] = Query(None),
    skill_id: Optional[str] = Query(None),
    judge_model: Optional[str] = Query(None),
    testcase_id: Optional[str] = Query(None),
    batch_id: Optional[str] = Query(None),
    sort: str = Query("created_at", description="Sort column; must be in allow-list"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Run)
    if status:
        q = q.filter(Run.status == status)
    if skill_id:
        q = q.filter(Run.skill_id == skill_id)
    if judge_model:
        q = q.filter(Run.judge_model == judge_model)
    if testcase_id:
        q = q.filter(Run.testcase_id == testcase_id)
    if batch_id:
        q = q.filter(Run.batch_id == batch_id)
    if sort not in _SORT_COLUMNS:
        raise HTTPException(400, f"sort must be one of: {sorted(_SORT_COLUMNS)}")
    sort_col = _SORT_COLUMNS[sort]
    sort_col = sort_col.desc() if order == "desc" else sort_col.asc()
    # Always tie-break by created_at desc so paginated results are stable.
    q = q.order_by(sort_col, Run.created_at.desc())
    total = q.with_entities(func.count(Run.id)).scalar() or 0
    rows = (
        q.offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total, "page": page, "page_size": page_size,
        "items": [RunBrief.model_validate(r).model_dump() for r in rows],
    }


@router.get("/runs/{run_id}", response_model=RunDetail)
def get_run(run_id: str, db: Session = Depends(get_db)):
    row = db.get(Run, run_id)
    if not row:
        raise HTTPException(404)
    return row


@router.post("/runs/{run_id}/rerun", response_model=RunBrief, status_code=201)
def rerun(run_id: str, bg: BackgroundTasks, db: Session = Depends(get_db)):
    prev = db.get(Run, run_id)
    if not prev:
        raise HTTPException(404)
    new = Run(
        testcase_id=prev.testcase_id,
        skill_id=prev.skill_id,
        judge_model=prev.judge_model,
        judge_provider=prev.judge_provider,
        status="pending", progress_pct=0, current_step="queued",
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    bg.add_task(evaluator.evaluate_run, new.id)
    return new


# ----------------------------------------------------------------------------
# Batches
# ----------------------------------------------------------------------------
@router.get("/runs/batches", response_model=list[RunBatchOut])
def list_batches(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200)):
    return db.query(RunBatch).order_by(RunBatch.created_at.desc()).limit(limit).all()


@router.get("/runs/batches/{batch_id}", response_model=RunBatchOut)
def get_batch(batch_id: str, db: Session = Depends(get_db)):
    b = db.get(RunBatch, batch_id)
    if not b:
        raise HTTPException(404)
    # Refresh aggregated counts (cheap)
    done = db.query(func.count(Run.id)).filter(Run.batch_id == batch_id, Run.status == "done").scalar() or 0
    failed = db.query(func.count(Run.id)).filter(Run.batch_id == batch_id, Run.status == "failed").scalar() or 0
    if b.done != done or b.failed != failed:
        b.done = done
        b.failed = failed
        db.commit()
        db.refresh(b)
    return b
