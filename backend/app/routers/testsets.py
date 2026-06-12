"""TestSets router — CRUD, disk scan, iwencai import."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import TestCase, TestCategory
from ..schemas import (
    IwencaiImportRequest,
    IwencaiImportResponse,
    ScanDiskResponse,
    TestCaseBrief,
    TestCaseCreate,
    TestCaseDetail,
    TestCaseUpdate,
    TestCategoryOut,
)
from ..services import fetch_iwencai
from ..services.skill_loader import SELF_SKILL_EN_SLUGS

router = APIRouter()


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
EN_PAT = re.compile(r"^[\x00-\x7F]+$")


def _detect_language(text: str) -> str:
    if not text:
        return "zh"
    chinese = sum(1 for c in text if "一" <= c <= "鿿")
    if chinese / max(len(text), 1) > 0.3:
        return "zh"
    if EN_PAT.match(text.strip()):
        return "en"
    return "mixed"


def _extract_tools(chain: Any) -> list[str]:
    out: set[str] = set()
    if not isinstance(chain, list):
        return []
    for step in chain:
        if not isinstance(step, dict):
            continue
        for t in step.get("tools") or []:
            if isinstance(t, dict) and t.get("name"):
                out.add(t["name"])
    return sorted(out)


def _infer_difficulty(text: str, chain: Any) -> str:
    steps = len(chain) if isinstance(chain, list) else 0
    n_tools = len(_extract_tools(chain))
    if steps <= 1 and n_tools <= 1 and len(text) < 200:
        return "simple"
    if steps >= 5 or n_tools >= 4 or len(text) > 2000:
        return "complex"
    return "medium"


def _has_charts(answer: str) -> bool:
    return "reference_v2" in (answer or "")


def _id_from_question(q: str) -> str:
    return "ans_" + hashlib.md5(q.encode("utf-8")).hexdigest()[:24]


def _normalize_raw(raw: dict) -> dict:
    """Accept both Chinese-keyed JSON (from 数据测试集) and English schema."""
    if "问题" in raw:
        return {
            "source_id": raw.get("id") or _id_from_question(raw["问题"]),
            "source": raw.get("来源", "iwencai"),
            "question": raw["问题"],
            "expected_answer": raw.get("答案", ""),
            "reasoning_trace": raw.get("链路数据") or [],
            "context_history": raw.get("上下文"),
        }
    return raw


# ----------------------------------------------------------------------------
# Categories
# ----------------------------------------------------------------------------
@router.get("/categories", response_model=list[TestCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(TestCategory).order_by(TestCategory.code).all()


# ----------------------------------------------------------------------------
# List / detail
# ----------------------------------------------------------------------------
@router.get("", response_model=dict)
def list_testcases(
    category: str | None = Query(None),
    language: str | None = Query(None),
    difficulty: str | None = Query(None),
    q: str | None = Query(None, description="full-text on question"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(TestCase)
    if category:
        query = query.filter(TestCase.category_code == category)
    if language:
        query = query.filter(TestCase.language == language)
    if difficulty:
        query = query.filter(TestCase.inferred_difficulty == difficulty)
    if q:
        query = query.filter(TestCase.question.ilike(f"%{q}%"))
    total = query.with_entities(func.count(TestCase.id)).scalar() or 0
    rows = (
        query.order_by(TestCase.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [TestCaseBrief.model_validate(r).model_dump() for r in rows],
    }


@router.get("/{tc_id}", response_model=TestCaseDetail)
def get_testcase(tc_id: str, db: Session = Depends(get_db)):
    row = db.get(TestCase, tc_id)
    if not row:
        raise HTTPException(404, f"TestCase {tc_id} not found")
    return row


# ----------------------------------------------------------------------------
# Create / update / delete
# ----------------------------------------------------------------------------
@router.post("", response_model=TestCaseDetail)
def create_testcase(body: TestCaseCreate, db: Session = Depends(get_db)):
    if not db.get(TestCategory, body.category_code):
        raise HTTPException(400, f"Category {body.category_code} unknown")
    tc = TestCase(
        source_id=body.source_id or _id_from_question(body.question),
        source=body.source,
        category_code=body.category_code,
        question=body.question,
        expected_answer=body.expected_answer,
        reasoning_trace=body.reasoning_trace,
        context_history=body.context_history,
        tags=body.tags,
        file_path=body.file_path,
        imported_from="manual",
        language=_detect_language(body.question),
        has_charts=_has_charts(body.expected_answer),
        tool_set=_extract_tools(body.reasoning_trace),
        inferred_difficulty=_infer_difficulty(body.expected_answer, body.reasoning_trace),
    )
    db.add(tc)
    db.commit()
    db.refresh(tc)
    return tc


@router.patch("/{tc_id}", response_model=TestCaseDetail)
def update_testcase(tc_id: str, body: TestCaseUpdate, db: Session = Depends(get_db)):
    tc = db.get(TestCase, tc_id)
    if not tc:
        raise HTTPException(404, f"TestCase {tc_id} not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(tc, k, v)
    if body.expected_answer is not None:
        tc.has_charts = _has_charts(body.expected_answer)
    if body.reasoning_trace is not None:
        tc.tool_set = _extract_tools(body.reasoning_trace)
        tc.inferred_difficulty = _infer_difficulty(tc.expected_answer or "", body.reasoning_trace)
    if body.question is not None:
        tc.language = _detect_language(body.question)
    db.commit()
    db.refresh(tc)
    return tc


@router.delete("/{tc_id}")
def delete_testcase(tc_id: str, db: Session = Depends(get_db)):
    tc = db.get(TestCase, tc_id)
    if not tc:
        raise HTTPException(404, f"TestCase {tc_id} not found")
    db.delete(tc)
    db.commit()
    return {"deleted": tc_id}


# ----------------------------------------------------------------------------
# Bulk import
# ----------------------------------------------------------------------------
@router.post("/import-file")
async def import_file(
    file: UploadFile = File(...),
    category_code: str = Query(...),
    db: Session = Depends(get_db),
):
    if not db.get(TestCategory, category_code):
        raise HTTPException(400, f"Category {category_code} unknown")
    content = (await file.read()).decode("utf-8")
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid JSON: {e}")
    raws = payload if isinstance(payload, list) else [payload]
    inserted = 0
    for raw in raws:
        norm = _normalize_raw(raw)
        if not norm.get("question"):
            continue
        existing = (
            db.query(TestCase)
            .filter_by(source_id=norm["source_id"], category_code=category_code)
            .first()
        )
        if existing:
            continue
        tc = TestCase(
            source_id=norm["source_id"],
            source=norm.get("source", "iwencai"),
            category_code=category_code,
            question=norm["question"],
            expected_answer=norm.get("expected_answer", ""),
            reasoning_trace=norm.get("reasoning_trace"),
            context_history=norm.get("context_history"),
            imported_from="file",
            language=_detect_language(norm["question"]),
            has_charts=_has_charts(norm.get("expected_answer", "")),
            tool_set=_extract_tools(norm.get("reasoning_trace")),
            inferred_difficulty=_infer_difficulty(
                norm.get("expected_answer", ""), norm.get("reasoning_trace")
            ),
        )
        db.add(tc)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "total_in_file": len(raws)}


@router.post("/import-from-iwencai", response_model=IwencaiImportResponse)
def import_from_iwencai(body: IwencaiImportRequest, db: Session = Depends(get_db)):
    """Pull samples from the iwencai EvalOps backend (internal-only)."""
    if not db.get(TestCategory, body.category_code):
        raise HTTPException(400, f"Category {body.category_code} unknown")
    try:
        records, failures = fetch_iwencai.fetch_many(body.record_ids)
    except RuntimeError as e:
        raise HTTPException(503, str(e))
    fails = [{"record_id": rid, "error": err} for rid, err in failures]
    inserted = 0
    for rec in records:
        norm = _normalize_raw(rec)
        existing = (
            db.query(TestCase)
            .filter_by(source_id=norm["source_id"], category_code=body.category_code)
            .first()
        )
        if existing:
            continue
        tc = TestCase(
            source_id=norm["source_id"],
            source=norm.get("source", "iwencai"),
            category_code=body.category_code,
            question=norm["question"],
            expected_answer=norm.get("expected_answer", ""),
            reasoning_trace=norm.get("reasoning_trace"),
            context_history=norm.get("context_history"),
            imported_from="fetch",
            language=_detect_language(norm["question"]),
            has_charts=_has_charts(norm.get("expected_answer", "")),
            tool_set=_extract_tools(norm.get("reasoning_trace")),
            inferred_difficulty=_infer_difficulty(
                norm.get("expected_answer", ""), norm.get("reasoning_trace")
            ),
        )
        db.add(tc)
        inserted += 1
    db.commit()
    return IwencaiImportResponse(imported=inserted, failed=fails)


@router.post("/scan-disk", response_model=ScanDiskResponse)
def scan_disk(db: Session = Depends(get_db)):
    """Walk the 数据测试集/ tree and upsert all *.json into the DB."""
    root: Path = settings.testsets_root_abs
    if not root.exists():
        raise HTTPException(500, f"Testsets root {root} does not exist")

    # ensure categories exist (skill_loader normally creates them, but be defensive)
    for code, slug in SELF_SKILL_EN_SLUGS.items():
        if not db.get(TestCategory, code):
            db.add(TestCategory(code=code, slug=slug, name_zh=slug, name_en=slug,
                                mapped_skill_id=f"self/{code}"))
    db.commit()

    scanned = 0
    inserted = 0
    updated = 0
    skipped = 0

    slug_to_code = {v: k for k, v in SELF_SKILL_EN_SLUGS.items()}
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        # category dirs look like "12-financial-logical-reasoning"
        m = re.match(r"^(\d{2})-(.+)$", sub.name)
        if m:
            code = m.group(1)
        else:
            slug = sub.name
            code = slug_to_code.get(slug)
            if not code:
                continue
        for f in sorted(sub.glob("*.json")):
            scanned += 1
            try:
                raw = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                skipped += 1
                continue
            norm = _normalize_raw(raw)
            if not norm.get("question"):
                skipped += 1
                continue
            existing = (
                db.query(TestCase)
                .filter_by(source_id=norm["source_id"], category_code=code)
                .first()
            )
            if existing:
                existing.question = norm["question"]
                existing.expected_answer = norm.get("expected_answer", "")
                existing.reasoning_trace = norm.get("reasoning_trace")
                existing.context_history = norm.get("context_history")
                existing.file_path = str(f)
                existing.language = _detect_language(norm["question"])
                existing.has_charts = _has_charts(norm.get("expected_answer", ""))
                existing.tool_set = _extract_tools(norm.get("reasoning_trace"))
                existing.inferred_difficulty = _infer_difficulty(
                    norm.get("expected_answer", ""), norm.get("reasoning_trace")
                )
                updated += 1
            else:
                tc = TestCase(
                    source_id=norm["source_id"],
                    source=norm.get("source", "iwencai"),
                    category_code=code,
                    question=norm["question"],
                    expected_answer=norm.get("expected_answer", ""),
                    reasoning_trace=norm.get("reasoning_trace"),
                    context_history=norm.get("context_history"),
                    file_path=str(f),
                    imported_from="file",
                    language=_detect_language(norm["question"]),
                    has_charts=_has_charts(norm.get("expected_answer", "")),
                    tool_set=_extract_tools(norm.get("reasoning_trace")),
                    inferred_difficulty=_infer_difficulty(
                        norm.get("expected_answer", ""), norm.get("reasoning_trace")
                    ),
                )
                db.add(tc)
                inserted += 1
    db.commit()
    return ScanDiskResponse(
        scanned=scanned, inserted=inserted, updated=updated, skipped=skipped,
    )
