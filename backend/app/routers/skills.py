"""Skills router — read-only Skill catalog + on-demand reload."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pathlib import Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

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


# ----------------------------------------------------------------------------
# Tree — list files under a skill's subdirectory
# ----------------------------------------------------------------------------
class SkillDirListing(BaseModel):
    dir: str
    files: List[str]  # rel paths from skill root


@router.get("/{skill_id:path}/tree", response_model=SkillDirListing)
def list_skill_dir(skill_id: str, dir: str = ""):
    """List files under `<skill_root>/<dir>`, returning rel paths.

    Used by the Skill Detail page to discover rubric/root-cause/tool-list
    files dynamically (so the UI doesn't hard-code the file list).

    Reuses the same path-traversal guard as /file: `..` is forbidden.
    """
    if ".." in dir:
        raise HTTPException(400, "dir must not contain '..'")
    loader = get_loader()
    rec = loader.get_one(skill_id)
    if not rec:
        raise HTTPException(404, f"Skill {skill_id} not found")
    base = Path(rec.path)
    target = base / dir
    if not target.exists():
        return SkillDirListing(dir=dir, files=[])
    if not target.is_dir():
        raise HTTPException(400, f"{dir} is not a directory")
    files: List[str] = []
    for f in sorted(target.iterdir()):
        if f.is_file() and f.suffix == ".md":
            files.append(str(f.relative_to(base)))
    return SkillDirListing(dir=dir, files=files)
