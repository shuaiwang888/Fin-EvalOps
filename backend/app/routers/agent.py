"""Data Agent router — conversational analytics over the eval database."""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import persistence as hf_persistence
from ..db import get_db
from ..models import AgentMessage, AgentSession
from ..schemas import (
    AgentMessageIn,
    AgentMessageOut,
    AgentSessionBrief,
    AgentSessionDetail,
)
from ..services import data_agent

router = APIRouter()


@router.get("/sessions", response_model=list[AgentSessionBrief])
def list_sessions(db: Session = Depends(get_db), limit: int = 20):
    return (
        db.query(AgentSession)
        .order_by(AgentSession.updated_at.desc())
        .limit(limit)
        .all()
    )


@router.post("/sessions", response_model=AgentSessionBrief, status_code=201)
def create_session(model: Optional[str] = None, db: Session = Depends(get_db)):
    sess = AgentSession(id=uuid.uuid4().hex, title="新对话", model=model or "")
    db.add(sess)
    db.commit()
    db.refresh(sess)
    hf_persistence.mark_dirty()
    return sess


@router.get("/sessions/{sid}", response_model=AgentSessionDetail)
def get_session(sid: str, db: Session = Depends(get_db)):
    sess = db.get(AgentSession, sid)
    if not sess:
        raise HTTPException(404)
    return sess


@router.delete("/sessions/{sid}")
def delete_session(sid: str, db: Session = Depends(get_db)):
    sess = db.get(AgentSession, sid)
    if not sess:
        raise HTTPException(404)
    db.delete(sess)
    db.commit()
    hf_persistence.mark_dirty()
    return {"deleted": sid}


@router.post("/sessions/{sid}/messages", response_model=dict)
def send_message(sid: str, body: AgentMessageIn, db: Session = Depends(get_db)):
    if not db.get(AgentSession, sid):
        raise HTTPException(404, "session not found")
    try:
        payload = data_agent.reply(
            sid,
            body.content,
            model_id=body.model,
            analysis_context=body.context.model_dump() if body.context else None,
        )
    except data_agent.AnalysisContextError as exc:
        raise HTTPException(404, str(exc)) from exc
    # data_agent.reply persists AgentMessage rows internally; mark dirty
    hf_persistence.mark_dirty()
    return payload


@router.get("/sessions/{sid}/messages", response_model=list[AgentMessageOut])
def list_messages(sid: str, db: Session = Depends(get_db)):
    sess = db.get(AgentSession, sid)
    if not sess:
        raise HTTPException(404)
    return sess.messages
