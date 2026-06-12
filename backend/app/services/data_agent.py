"""Data Agent — natural-language conversation over the SQLite database.

Two-stage flow:
1. LLM decides whether to issue a read-only SQL query OR a chart spec OR
   pure text answer. Output is a structured tool call.
2. We execute the SQL safely (forbid INSERT/UPDATE/DELETE/DROP, single-statement,
   row cap 200), then loop the result back to the LLM for the final answer.

Read-only by construction: we open a separate SQLite connection in
`read_only=true` mode.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from ..config import settings
from ..db import db_session
from ..models import AgentMessage, AgentSession
from ..utils.trace import get_logger
from . import llm_client

log = get_logger(__name__)


DB_SCHEMA_BRIEF = """
表结构(SQLite,只读):

skills(id, family, code, name_zh, name_en, schema_version, one_liner, golden_case_count)
  · family ∈ {'self','competitor','e2e'}, code ∈ '01'..'14'
test_categories(code, slug, name_zh, name_en, mapped_skill_id)
  · 13 个测试集分类
testcases(id, source_id, category_code, question, language, has_charts,
          inferred_difficulty, tags, imported_from, created_at)
runs(id, batch_id, testcase_id, skill_id, judge_model, judge_provider,
     status, final_score, absolute_score_pre_cap,
     latency_ms, tokens_in, tokens_out, cost_usd,
     created_at, finished_at, error_msg)
  · status ∈ {pending,routing,running,scoring,done,failed,cancelled}
  · final_score ∈ [0, 100]
run_batches(id, label, judge_model, total, done, failed, created_at)
annotations(id, run_id, reviewer, is_golden, created_at)

注意:
- runs.routing / dimension_scores / caps / root_causes / narrative_review 是 JSON 列,SQLite 用 json_extract 读取
- 想看趋势用 strftime('%Y-%m-%d', created_at)
- 想看根因 L1 分布: json_extract(root_causes, '$[0].l1')
"""

AGENT_SYSTEM = """你是 Fin-EvalOps 平台的「数据分析助手」。用户会用中文问你评测数据的问题,你需要:
1. 如果问题涉及具体数据,先生成一个 **SELECT** SQL(SQLite 方言),禁止 INSERT/UPDATE/DELETE/DROP/PRAGMA
2. 如果需要画图,同时输出 `chart_spec`(ECharts option JSON 片段,字段 type/title/xField/yField/series 等)
3. 如果只是闲聊或概念解释,只填 `answer`,SQL 留空

数据库结构:
""" + DB_SCHEMA_BRIEF + """

返回 JSON 严格遵守:
{
  "answer": "<给用户的最终中文回答>",
  "sql": "<可选,SELECT 语句,行数限 200>",
  "chart_spec": {<可选 ECharts option>}
}
"""

AGENT_SCHEMA = {
    "type": "object",
    "required": ["answer"],
    "additionalProperties": True,
    "properties": {
        "answer": {"type": "string", "maxLength": 4000},
        "sql": {"type": ["string", "null"]},
        "chart_spec": {"type": ["object", "null"]},
    },
}


# Forbidden tokens (case-insensitive whole-word check).
# `detach` and `reindex`/`analyze` are added because SQLite treats them as
# side-effecting without going through `DROP`/`CREATE`.
_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|truncate|alter|create|attach|detach|"
    r"pragma|vacuum|replace|reindex|analyze|load|savepoint|release)\b",
    re.IGNORECASE,
)


# Cache the read-only engine so we don't recreate the pool on every query.
_ro_engine: Engine | None = None
_ro_engine_uri: str | None = None


def _read_only_engine() -> Engine:
    """SQLite engine opened in read-only mode (cached)."""
    global _ro_engine, _ro_engine_uri
    path = settings.db_path_abs
    uri = f"sqlite:///file:{path}?mode=ro&uri=true"
    if _ro_engine is None or _ro_engine_uri != uri:
        _ro_engine = create_engine(
            uri, future=True, connect_args={"uri": True, "check_same_thread": False}
        )
        _ro_engine_uri = uri
    return _ro_engine


def _execute_sql(sql: str, row_cap: int = 200) -> List[Dict[str, Any]]:
    if _FORBIDDEN.search(sql):
        raise ValueError("SQL 中包含被禁止的关键字(只允许 SELECT)")
    if ";" in sql.strip().rstrip(";"):
        raise ValueError("仅允许单条 SELECT 语句")
    if not re.match(r"^\s*(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("仅允许 SELECT/WITH 开头的查询")

    eng = _read_only_engine()
    with eng.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows[:row_cap]]


def _build_history(session_id: str) -> List[dict]:
    with db_session() as db:
        sess = db.get(AgentSession, session_id)
        if not sess:
            return []
        msgs: list[dict] = []
        for m in sess.messages[-12:]:  # cap context
            if m.role == "user":
                msgs.append({"role": "user", "content": m.content})
            elif m.role == "assistant":
                msgs.append({"role": "assistant", "content": m.content})
        return msgs


def reply(session_id: str, user_text: str, model_id: Optional[str] = None) -> dict:
    """Process one user turn — returns the assistant payload (also persisted)."""
    with db_session() as db:
        sess = db.get(AgentSession, session_id)
        if not sess:
            sess = AgentSession(id=session_id, title=user_text[:60], model=model_id or "")
            db.add(sess)
            db.flush()
        user_msg = AgentMessage(session_id=sess.id, role="user", content=user_text)
        db.add(user_msg)
        if not sess.title or sess.title == "New conversation":
            sess.title = user_text[:60]

    history = _build_history(session_id)
    history.append({"role": "user", "content": user_text})

    result = llm_client.call_with_schema(
        model_id=model_id,
        system=AGENT_SYSTEM,
        user=json.dumps({"history": history}, ensure_ascii=False),
        schema=AGENT_SCHEMA,
        tool_name="reply",
        max_tokens=2048,
        temperature=0.3,
    )
    payload = result.data
    sql = (payload.get("sql") or "").strip()
    data_preview: list[dict] = []
    if sql:
        try:
            data_preview = _execute_sql(sql)
            payload["row_count"] = len(data_preview)
        except Exception as exc:
            payload["sql_error"] = str(exc)
            log.warning("Data Agent SQL failed: %s | sql=%s", exc, sql[:200])

    with db_session() as db:
        am = AgentMessage(
            session_id=session_id,
            role="assistant",
            content=payload.get("answer", ""),
            sql_used=sql or None,
            chart_spec=payload.get("chart_spec"),
            data_preview=data_preview or None,
        )
        db.add(am)
        sess = db.get(AgentSession, session_id)
        if sess:
            sess.updated_at = datetime.now(timezone.utc)
    payload["data_preview"] = data_preview
    return payload
