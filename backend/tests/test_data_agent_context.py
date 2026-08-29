from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db import Base
from app import models
from app.services import data_agent
from app.services.llm_client import LLMResult


def _result(data: dict) -> LLMResult:
    return LLMResult(
        data=data,
        raw_text="",
        tokens_in=1,
        tokens_out=1,
        latency_ms=1,
        model="test-model",
        provider="test",
    )


def test_data_agent_executes_sql_then_synthesizes_with_real_rows(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add(models.AgentSession(id="session", title="新对话", model="test-model"))
        db.commit()

    @contextmanager
    def session_scope():
        with Session(engine) as db:
            try:
                yield db
                db.commit()
            except Exception:
                db.rollback()
                raise

    calls: list[dict] = []

    def fake_call(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return _result({
                "answer": "准备查询",
                "sql": "SELECT status, count(*) AS n FROM runs GROUP BY status",
                "chart_spec": None,
            })
        assert '"rows": [{"status": "failed", "n": 3}]' in kwargs["user"]
        return _result({"answer": "共有 3 条失败记录，主要应先处理执行异常。"})

    monkeypatch.setattr(data_agent, "db_session", session_scope)
    monkeypatch.setattr(data_agent, "_execute_sql", lambda sql: [{"status": "failed", "n": 3}])
    monkeypatch.setattr(data_agent, "_load_analysis_context", lambda context: {"scope": "category"})
    monkeypatch.setattr(data_agent.llm_client, "call_with_schema", fake_call)

    payload = data_agent.reply(
        "session",
        "这个分类失败了多少条？",
        analysis_context={"scope": "category", "category_code": "01"},
    )

    assert len(calls) == 2
    assert payload["answer"].startswith("共有 3 条失败记录")
    assert payload["row_count"] == 1
    assert payload["data_preview"] == [{"status": "failed", "n": 3}]

    with Session(engine) as db:
        session = db.get(models.AgentSession, "session")
        assert session.title == "这个分类失败了多少条？"
        assert [message.role for message in session.messages] == ["user", "assistant"]


def test_testcase_context_contains_details_and_distinguishes_failed_runs(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add(models.TestCategory(code="01", slug="one", name_zh="事件选股", name_en="one"))
        db.add(models.TestCase(
            id="tc", source_id="source", source="manual", category_code="01",
            question="哪些股票受益？", agent_answer="回答内容",
            reasoning_trace=[{"step": 1}], language="zh",
            inferred_difficulty="medium", imported_from="manual",
        ))
        db.add(models.Run(
            id="run", testcase_id="tc", skill_id="self/01",
            judge_model="m", judge_provider="p", status="failed",
            error_msg="Judge 输出不完整",
        ))
        db.commit()

    @contextmanager
    def session_scope():
        with Session(engine) as db:
            yield db

    monkeypatch.setattr(data_agent, "db_session", session_scope)
    context = data_agent._load_analysis_context({"scope": "testcase", "testcase_id": "tc"})

    assert context["testcase"]["question"] == "哪些股票受益？"
    assert context["testcase"]["agent_answer"] == "回答内容"
    assert context["evaluation_runs"][0]["status"] == "failed"
    assert context["evaluation_runs"][0]["final_score"] is None


def test_data_agent_caps_rows_inside_database(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(data_agent, "_read_only_engine", lambda: engine)

    rows = data_agent._execute_sql(
        """WITH RECURSIVE numbers(n) AS (
               SELECT 1 UNION ALL SELECT n + 1 FROM numbers WHERE n < 300
           ) SELECT n FROM numbers ORDER BY n""",
        row_cap=25,
    )

    assert len(rows) == 25
    assert rows[0] == {"n": 1}
    assert rows[-1] == {"n": 25}
