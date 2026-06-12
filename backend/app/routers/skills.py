"""Skills router — read-only Skill catalog + on-demand reload."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Skill
from ..schemas import ReloadSkillsResponse, SkillBrief, SkillDetail
from ..services.skill_loader import get_loader, reset_loader

router = APIRouter()


@router.get("", response_model=list[SkillBrief])
def list_skills(
    family: str | None = Query(None, pattern="^(self|competitor|e2e)$"),
    db: Session = Depends(get_db),
):
    q = db.query(Skill).order_by(Skill.family, Skill.code)
    if family:
        q = q.filter(Skill.family == family)
    return q.all()


@router.get("/{skill_id:path}", response_model=SkillDetail)
def get_skill(skill_id: str, db: Session = Depends(get_db)):
    row = db.get(Skill, skill_id)
    if not row:
        raise HTTPException(404, f"Skill {skill_id} not found")
    return row


@router.get("/{skill_id:path}/file")
def get_skill_file(skill_id: str, rel: str = Query(..., description="Relative path within skill dir")):
    """Return raw markdown of a sub-file (rubric/_index.md, cap_*.md, etc.)."""
    if ".." in rel:
        raise HTTPException(400, "rel must not contain '..'")
    loader = get_loader()
    try:
        text = loader.read_skill_file(skill_id, rel)
    except FileNotFoundError:
        raise HTTPException(404, f"Skill {skill_id} not found")
    if not text:
        raise HTTPException(404, f"{rel} not found in skill {skill_id}")
    return {"skill_id": skill_id, "rel": rel, "content": text}


@router.post("/reload", response_model=ReloadSkillsResponse)
def reload_skills():
    reset_loader()
    loader = get_loader()
    n = loader.sync_to_db()
    families = {"self": 0, "competitor": 0, "e2e": 0}
    for r in loader.scan_all():
        families[r.family] = families.get(r.family, 0) + 1
    return ReloadSkillsResponse(
        self=families["self"], competitor=families["competitor"],
        e2e=families["e2e"], total=n,
    )
