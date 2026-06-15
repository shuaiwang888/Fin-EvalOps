"""Annotations router — P1 human review and golden marking."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import persistence as hf_persistence
from ..db import get_db
from ..models import Annotation, Run
from ..schemas import AnnotationCreate, AnnotationOut

router = APIRouter()


@router.post("", response_model=AnnotationOut, status_code=201)
def create_annotation(body: AnnotationCreate, db: Session = Depends(get_db)):
    if not db.get(Run, body.run_id):
        raise HTTPException(404, f"Run {body.run_id} not found")
    a = Annotation(
        run_id=body.run_id,
        reviewer=body.reviewer,
        dim_overrides=body.dim_overrides,
        comment=body.comment,
        is_golden=body.is_golden,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    hf_persistence.mark_dirty()
    return a


@router.get("", response_model=list[AnnotationOut])
def list_annotations(
    run_id: str | None = Query(None),
    is_golden: bool | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Annotation)
    if run_id:
        q = q.filter(Annotation.run_id == run_id)
    if is_golden is not None:
        q = q.filter(Annotation.is_golden == is_golden)
    return q.order_by(Annotation.created_at.desc()).all()


@router.delete("/{aid}")
def delete_annotation(aid: str, db: Session = Depends(get_db)):
    a = db.get(Annotation, aid)
    if not a:
        raise HTTPException(404)
    db.delete(a)
    db.commit()
    hf_persistence.mark_dirty()
    return {"deleted": aid}
