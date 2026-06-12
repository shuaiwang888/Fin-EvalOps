"""Dashboard router — aggregate KPIs, trend, top failures."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Run, Skill, TestCase
from ..schemas import DashboardSummary, DashboardTrendPoint, TopFailureRow
from ..services import llm_client

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db)):
    total_testcases = db.query(func.count(TestCase.id)).scalar() or 0
    total_runs = db.query(func.count(Run.id)).filter(Run.status == "done").scalar() or 0
    avg = db.query(func.avg(Run.final_score)).filter(Run.status == "done").scalar()
    pass_rate = (
        db.query(
            func.avg(case((Run.final_score >= 60, 1.0), else_=0.0))
        ).filter(Run.status == "done").scalar()
    )

    by_skill_rows = (
        db.query(
            Run.skill_id,
            func.count(Run.id).label("n"),
            func.avg(Run.final_score).label("avg_score"),
        )
        .filter(Run.status == "done")
        .group_by(Run.skill_id)
        .all()
    )
    skill_lookup = {s.id: s for s in db.query(Skill).all()}
    by_skill = [
        {
            "skill_id": r.skill_id,
            "name_zh": skill_lookup[r.skill_id].name_zh if r.skill_id in skill_lookup else r.skill_id,
            "count": r.n,
            "avg_score": round(float(r.avg_score), 2) if r.avg_score is not None else None,
        }
        for r in by_skill_rows
    ]

    # L1 root cause distribution — extract from JSON
    by_l1: dict[str, int] = {}
    for row in db.query(Run.root_causes).filter(
        Run.status == "done", Run.root_causes.isnot(None)
    ).all():
        rc = row[0] or []
        for item in rc:
            l1 = (item or {}).get("l1")
            if l1:
                by_l1[l1] = by_l1.get(l1, 0) + 1
    by_l1_list = sorted(
        [{"l1": k, "count": v} for k, v in by_l1.items()],
        key=lambda r: -r["count"],
    )[:10]

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    last_24h = db.query(func.count(Run.id)).filter(Run.created_at >= since).scalar() or 0

    available_models = [m["id"] for m in llm_client.list_models()]
    return DashboardSummary(
        total_testcases=total_testcases,
        total_runs=total_runs,
        avg_score=round(float(avg), 2) if avg is not None else None,
        pass_rate=round(float(pass_rate), 4) if pass_rate is not None else None,
        by_skill=by_skill,
        by_l1_root_cause=by_l1_list,
        available_models=available_models,
        available_providers=sorted({m["provider"] for m in llm_client.list_models()}),
        last_24h_runs=last_24h,
    )


@router.get("/trend", response_model=list[DashboardTrendPoint])
def trend(
    days: int = Query(30, ge=1, le=365),
    skill_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = db.query(
        func.strftime("%Y-%m-%d", Run.created_at).label("d"),
        Run.skill_id,
        func.avg(Run.final_score).label("avg_score"),
        func.count(Run.id).label("n"),
    ).filter(Run.status == "done", Run.created_at >= since)
    if skill_id:
        q = q.filter(Run.skill_id == skill_id)
    q = q.group_by("d", Run.skill_id).order_by("d")
    return [
        DashboardTrendPoint(
            date=r.d, skill_id=r.skill_id,
            avg_score=round(float(r.avg_score), 2) if r.avg_score is not None else 0.0,
            count=r.n,
        )
        for r in q.all()
    ]


@router.get("/top-failures", response_model=list[TopFailureRow])
def top_failures(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    rows = (
        db.query(Run, TestCase)
        .join(TestCase, Run.testcase_id == TestCase.id)
        .filter(Run.status == "done")
        .order_by(Run.final_score.asc().nulls_last(), Run.created_at.desc())
        .limit(limit)
        .all()
    )
    out: list[TopFailureRow] = []
    for run, tc in rows:
        caps = [c.get("rule_id") for c in (run.caps or []) if c.get("triggered")]
        top_l1 = None
        rcs = run.root_causes or []
        if rcs:
            ranked = sorted(rcs, key=lambda r: (r or {}).get("raw_score", 100))
            if ranked:
                top_l1 = ranked[0].get("l1")
        out.append(TopFailureRow(
            run_id=run.id, testcase_id=tc.id,
            question_preview=tc.question[:80],
            skill_id=run.skill_id,
            final_score=float(run.final_score or 0),
            caps_triggered=caps,
            top_root_cause=top_l1,
            created_at=run.created_at,
        ))
    return out


@router.get("/skill-coverage")
def skill_coverage(db: Session = Depends(get_db)):
    """Average score for each of 13 self-eval skills + sample count per
    category (used for the dashboard radar)."""
    rows = (
        db.query(
            Run.skill_id,
            func.avg(Run.final_score).label("avg_score"),
            func.count(Run.id).label("n"),
        )
        .filter(Run.status == "done", Run.skill_id.like("self/%"))
        .group_by(Run.skill_id)
        .all()
    )
    skills = {s.id: s for s in db.query(Skill).filter(Skill.family == "self").all()}
    by_skill = {r.skill_id: r for r in rows}
    out = []
    for sid, s in sorted(skills.items(), key=lambda kv: kv[1].code):
        r = by_skill.get(sid)
        out.append({
            "skill_id": sid,
            "code": s.code,
            "name_zh": s.name_zh,
            "avg_score": round(float(r.avg_score), 2) if r and r.avg_score is not None else None,
            "count": r.n if r else 0,
        })
    return out
