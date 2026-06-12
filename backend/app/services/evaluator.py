"""Evaluator — runs the 5-step protocol against a (TestCase, Skill) pair.

Sync function intended to be called from a BackgroundTask. Emits SSE
events at every protocol step so the UI can render progress live.

The judge LLM returns structured JSON conforming to a per-Skill schema we
synthesise from the README + output-schema_zh.md. We deliberately keep that
schema loose (additionalProperties allowed at the leaf level) because each
of the 13 Skills uses slightly different dimension names — strict
enumeration would require maintaining 13 hard-coded lists.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from ..db import db_session
from ..models import Run, Skill, TestCase
from ..utils.prompts import EVALUATOR_SYSTEM
from ..utils.trace import get_logger, set_trace_id
from . import llm_client, scorer, skill_router
from .skill_loader import get_loader
from .sse_broker import broker

log = get_logger(__name__)


# ============================================================================
# JSON Schema — purposely tolerant; the 13 Skills share core fields
# ============================================================================
EVAL_OUTPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": [
        "schema_version", "weight_assignment", "dimension_scores",
        "caps", "root_causes", "narrative_review",
    ],
    "additionalProperties": True,
    "properties": {
        "schema_version": {"type": "string"},
        "weight_assignment": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["dynamic_weight", "applicability"],
                "additionalProperties": True,
                "properties": {
                    "dynamic_weight": {"type": "integer", "minimum": 0, "maximum": 100},
                    "applicability": {
                        "type": "string",
                        "enum": ["relevant", "supplementary", "not_applicable"],
                    },
                    "rationale": {"type": "string"},
                },
            },
        },
        "skipped_dimensions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "dimension": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "matched_golden_cases": {
            "type": "array",
            "items": {"type": "string"},
        },
        "dimension_scores": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["raw_score"],
                "additionalProperties": True,
                "properties": {
                    "raw_score": {"type": "number", "minimum": 0, "maximum": 100},
                    "evidence": {"type": "array"},
                },
            },
        },
        "caps": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": True,
                "required": ["rule_id", "triggered"],
                "properties": {
                    "rule_id": {"type": "string"},
                    "triggered": {"type": "boolean"},
                    "score_ceiling": {"type": "number"},
                    "reason": {"type": "string"},
                    "evidence": {"type": "array"},
                },
            },
        },
        "root_causes": {
            "type": "array",
            "maxItems": 10,
            "items": {
                "type": "object",
                "additionalProperties": True,
                "required": ["l1"],
                "properties": {
                    "l1": {"type": "string"},
                    "l2": {"type": "string"},
                    "dimension": {"type": "string"},
                    "raw_score": {"type": "number"},
                    "confidence": {"type": "string"},
                    "summary": {"type": "string"},
                    "evidence": {"type": "array"},
                },
            },
        },
        "narrative_review": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "summary": {"type": "string"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
                "next_actions": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}


# ============================================================================
def evaluate_run(run_id: str) -> None:
    """Background entrypoint — full 5-step protocol for one Run."""
    set_trace_id(run_id[:8])
    log.info("Starting evaluation run=%s", run_id)
    channel = f"runs/{run_id}"

    try:
        with db_session() as db:
            run = db.get(Run, run_id)
            if not run:
                log.error("Run %s vanished", run_id)
                return
            testcase = db.get(TestCase, run.testcase_id)
            skill_row = db.get(Skill, run.skill_id)
            if not testcase or not skill_row:
                _fail(db, run, channel, "Testcase or Skill missing")
                return

            # 1. routing — only run auto-router if not pre-decided (user-supplied skill_id)
            if not run.routing:
                _emit(channel, "step", {"step": -1, "label": "路由判定"})
                r = skill_router.route(
                    testcase.question,
                    judge_model=run.judge_model,
                    hint_skill_id=run.skill_id,
                )
                run.routing = {
                    "predicted_skill": r.skill_code,
                    "skill_id": r.skill_id,
                    "confidence": r.confidence,
                    "reasoning": r.reasoning,
                    "alternatives": r.alternatives,
                    "stage_used": r.stage_used,
                    "fallback": r.fallback,
                }
                # If auto-router picked a different skill than pre-specified, follow the
                # user intent (run.skill_id) but record the router's view in `routing`
                # so the UI can show why there was a divergence.
                if run.skill_id and run.skill_id != r.skill_id:
                    run.routing["overridden_to"] = run.skill_id
                db.commit()

            # 2. load skill protocol
            loader = get_loader()
            bundle = loader.load_protocol_bundle(skill_row.id)
            _emit(channel, "step", {"step": 0, "label": "分析题目 + 加载协议"})
            _update(db, run, channel, status="running", progress=10, current_step="step0")

            # 3. compose prompt
            system = EVALUATOR_SYSTEM.format(
                skill_protocol=bundle.get("skill", ""),
                rubric_index=bundle.get("rubric_index", ""),
                rubric_raw_scale=bundle.get("rubric_raw_scale", ""),
                caps=bundle.get("caps", ""),
                root_cause=bundle.get("root_cause", ""),
                tool_list=bundle.get("tool_list", ""),
                output_schema=bundle.get("output_schema", ""),
                golden_cases=bundle.get("golden_cases", "")[:6000],  # trim very long
            )
            tool_set = _extract_tool_set(testcase.reasoning_trace)
            user_payload = {
                "question": testcase.question,
                "text_answer": testcase.expected_answer,
                "context": testcase.context_history,
                "chain": testcase.reasoning_trace,
                "tools": list(tool_set),
                "timing": None,
                "meta": {"user_investment_goal": None},
            }

            _emit(channel, "step", {"step": 1, "label": "盲评最终答案 → LLM 调用中"})
            _update(db, run, channel, status="running", progress=35, current_step="step1")

            # 4. call judge LLM
            try:
                result = llm_client.call_with_schema(
                    model_id=run.judge_model,
                    system=system,
                    user=user_payload,
                    schema=EVAL_OUTPUT_SCHEMA,
                    tool_name="submit_evaluation",
                    max_tokens=6000,
                    temperature=0.15,
                )
            except llm_client.SchemaValidationError as exc:
                _fail(db, run, channel, f"判分输出不符合 schema:{exc}")
                return
            except Exception as exc:
                _fail(db, run, channel, f"LLM 调用失败:{exc}")
                return

            run.judge_provider = result.provider
            run.tokens_in = result.tokens_in
            run.tokens_out = result.tokens_out
            run.latency_ms = result.latency_ms
            data = result.data

            _emit(channel, "step", {"step": 2, "label": "链路诊断 + 根因归因"})
            _update(db, run, channel, status="scoring", progress=70, current_step="step2")

            run.raw_response = data
            run.weight_assignment = data.get("weight_assignment")
            run.dimension_scores = data.get("dimension_scores")
            run.caps = data.get("caps")
            run.root_causes = data.get("root_causes")
            run.narrative_review = data.get("narrative_review")
            run.matched_golden_cases = data.get("matched_golden_cases")
            run.skipped_dimensions = data.get("skipped_dimensions")

            _emit(channel, "step", {"step": 3, "label": "应用封顶规则"})
            _update(db, run, channel, status="scoring", progress=85, current_step="step3")

            sc = scorer.compute_scores(
                run.weight_assignment, run.dimension_scores, run.caps,
            )
            run.absolute_score_pre_cap = sc.absolute_score_pre_cap
            run.final_score = sc.final_score

            _emit(channel, "step", {"step": 4, "label": "序列化输出"})
            _update(db, run, channel, status="done", progress=100,
                    current_step="done", finished_at=datetime.now(timezone.utc))

            _emit(channel, "complete", {
                "run_id": run.id,
                "final_score": sc.final_score,
                "absolute_score_pre_cap": sc.absolute_score_pre_cap,
                "warnings": sc.warnings,
                "triggered_caps": [c.get("rule_id") for c in sc.triggered_caps],
            })
    except Exception as exc:  # safety net
        log.exception("Evaluator crashed: %s", exc)
        try:
            with db_session() as db:
                run = db.get(Run, run_id)
                if run:
                    _fail(db, run, channel, f"评测器异常:{exc}")
        except Exception:  # pragma: no cover
            pass
    finally:
        broker.close(channel)


# ----------------------------------------------------------------------------
def _emit(channel: str, event: str, data: dict) -> None:
    broker.publish(channel, event, data)


def _update(db: Session, run: Run, channel: str, *, status: str, progress: int,
            current_step: str, finished_at: Optional[datetime] = None) -> None:
    """Mutate the run row and emit an SSE progress event.

    Caller is responsible for committing the surrounding transaction
    (we use `db_session()` which auto-commits on exit). Avoids double-commit.
    """
    run.status = status
    run.progress_pct = progress
    run.current_step = current_step
    if finished_at:
        run.finished_at = finished_at
    _emit(channel, "progress",
          {"status": status, "progress": progress, "current_step": current_step})


def _fail(db: Session, run: Run, channel: str, msg: str) -> None:
    log.error("Run %s failed: %s", run.id, msg)
    run.status = "failed"
    run.error_msg = msg
    run.finished_at = datetime.now(timezone.utc)
    # Caller's `db_session()` will commit on exit
    _emit(channel, "error", {"run_id": run.id, "message": msg})


def _extract_tool_set(chain: Any) -> set[str]:
    out: set[str] = set()
    if not isinstance(chain, list):
        return out
    for step in chain:
        if not isinstance(step, dict):
            continue
        for tool in step.get("tools") or []:
            if isinstance(tool, dict) and tool.get("name"):
                out.add(str(tool["name"]))
    return out


# ============================================================================
def evaluate_batch(batch_id: str, run_ids: list[str]) -> None:
    """Run many evaluations sequentially (provider rate limits forbid full
    parallelism for the free MVP). Emits batch-level progress."""
    set_trace_id(f"batch-{batch_id[:6]}")
    channel = f"batches/{batch_id}"
    log.info("Batch %s: %d runs", batch_id, len(run_ids))
    for idx, rid in enumerate(run_ids):
        try:
            evaluate_run(rid)
        except Exception as exc:
            log.exception("Batch %s: run %s failed: %s", batch_id, rid, exc)
        _emit(channel, "progress", {
            "index": idx + 1, "total": len(run_ids), "run_id": rid,
        })
    broker.close(channel)
