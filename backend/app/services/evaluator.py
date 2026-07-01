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

from .. import config as app_config
from ..db import db_session

# Capture at module load; we read the env-tunable concurrency from here so
# tests can monkey-patch it. The default of 3 is conservative — most LLM
# providers rate-limit per API key, and 3 concurrent eval calls is a
# sweet spot for minimax / anthropic free tiers without hitting 429s.
settings = app_config.settings
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
                "text_answer": testcase.agent_answer,
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
                    max_tokens=16000,  # bumped from 8000 — long answers + many
                                       # root_causes can overflow the budget; if
                                       # still truncated the call raises
                                       # LLMTruncatedError (caught below)
                    temperature=0.15,
                )
            except llm_client.SchemaValidationError as exc:
                _fail(db, run, channel, f"判分输出不符合 schema:{exc}")
                return
            except llm_client.LLMTruncatedError as exc:
                _fail(db, run, channel,
                      f"LLM 输出超过 16000 token 上限被截断,放弃本次评测:"
                      f"{exc}。可联系管理员提升上限或精简输入。")
                return
            except Exception as exc:
                _fail(db, run, channel, f"LLM 调用失败:{exc}")
                return

            run.judge_provider = result.provider
            run.tokens_in = result.tokens_in
            run.tokens_out = result.tokens_out
            run.latency_ms = result.latency_ms
            data = result.data

            # ---- 4.5 Sanitize common LLM structural mistakes ----
            # Some providers (esp. Anthropic-compatible endpoints) misinterpret
            # `additionalProperties` schemas and return arrays or wrapped objects.
            # We coerce here so a single bad shape doesn't fail the whole run.
            data = _sanitize_judge_output(data, channel, skill_row=skill_row)

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

            scorer_failed = False
            triggered_caps: list = []
            warnings: list = []
            try:
                sc = scorer.compute_scores(
                    run.weight_assignment, run.dimension_scores, run.caps,
                )
                run.absolute_score_pre_cap = sc.absolute_score_pre_cap
                run.final_score = sc.final_score
                triggered_caps = [c.get("rule_id") for c in sc.triggered_caps if isinstance(c, dict)]
                warnings = sc.warnings
            except Exception as exc:
                # Scorer raised on a malformed judge output (e.g. list-where-dict
                # despite all the sanitization above). Don't kill the whole run —
                # record the raw response and an error_msg so the user can still
                # inspect what came back, but mark status='failed' for clarity.
                log.exception("Scorer crashed on run %s: %s", run.id, exc)
                run.status = "failed"
                run.error_msg = f"判分计算异常:{exc}"
                run.finished_at = datetime.now(timezone.utc)
                run.absolute_score_pre_cap = None
                run.final_score = None
                _emit(channel, "error", {
                    "run_id": run.id,
                    "message": run.error_msg,
                })
                scorer_failed = True

            if not scorer_failed:
                _emit(channel, "step", {"step": 4, "label": "序列化输出"})
                _update(db, run, channel, status="done", progress=100,
                        current_step="done", finished_at=datetime.now(timezone.utc))

                _emit(channel, "complete", {
                    "run_id": run.id,
                    "final_score": sc.final_score,
                    "absolute_score_pre_cap": sc.absolute_score_pre_cap,
                    "warnings": warnings,
                    "triggered_caps": triggered_caps,
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
    # Coarse "something changed" signal — the actual upload is amortized
    # (batch-end / periodic / shutdown) so this is safe to call per row.
    try:
        from .. import persistence
        persistence.mark_dirty()
    except Exception:
        pass


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
# Known field names per judge-output field. Anything else in an entry is
# treated as the dimension name (or a fallback positional name is used).
_WEIGHT_FIELDS = {"dynamic_weight", "applicability", "rationale"}
_DIM_SCORE_FIELDS = {"raw_score", "evidence", "confidence", "summary"}
# Explicit keys some judge models use to label the dimension inside an entry.
_DIM_NAME_KEYS = ("dim_name", "name", "dimension", "key", "id", "label")


def _resolve_dim_names(data: dict, n: int, skill_row=None) -> list[str]:
    """Best-effort list of dimension names for positional mapping.

    Priority:
    1. Skill row's `dimensions.items[].label` (when known — gives the
       canonical order and human-readable names).
    2. Keys already unwrapped from weight_assignment.
    3. Generic `dim_0`, `dim_1`, ... placeholders.
    """
    # 1) Try skill spec
    if skill_row is not None:
        dims = skill_row.dimensions if isinstance(skill_row.dimensions, dict) else None
        items = (dims or {}).get("items") if dims else None
        if isinstance(items, list) and items:
            labels: list[str] = []
            for it in items:
                lbl = it.get("label") if isinstance(it, dict) else None
                if lbl:
                    labels.append(str(lbl))
            if labels:
                return labels[:n] if len(labels) >= n else labels + [
                    f"dim_{i}" for i in range(len(labels), n)
                ]
    # 2) Use whatever keys we already have in weight_assignment
    wa = data.get("weight_assignment")
    if isinstance(wa, dict):
        existing = [k for k in wa.keys() if k != "item"]
        if existing:
            return existing[:n] + [
                f"dim_{i}" for i in range(len(existing), n)
            ]
    # 3) Placeholder
    return [f"dim_{i}" for i in range(n)]


def _unwrap_item_array(
    field_data: dict,
    known_fields: set[str],
    fallback_dim_names: list[str],
) -> tuple[dict, int]:
    """Unwrap `{"item": [entry, ...]}` into a flat dict {dim_name: {...}}.

    Returns (flattened_dict, n_items_unwrapped).
    Each entry's dim_name is found via:
    1. Explicit dim-name key (any key not in known_fields)
    2. Common dim-name keys (dim_name, name, dimension, ...)
    3. Positional fallback to `fallback_dim_names[i]`
    """
    items = field_data.get("item")
    if not isinstance(items, list):
        return field_data, 0

    out: dict = {}
    for i, entry in enumerate(items):
        if not isinstance(entry, dict):
            continue
        # Find dim_name
        dim_name = None
        extra = [k for k in entry.keys() if k not in known_fields]
        if extra:
            dim_name = extra[0]
        if dim_name is None:
            for k in _DIM_NAME_KEYS:
                if k in entry and isinstance(entry[k], str):
                    dim_name = entry[k]
                    break
        if dim_name is None and i < len(fallback_dim_names):
            dim_name = fallback_dim_names[i]
        if dim_name is None:
            dim_name = f"dim_{i}"

        clean = {k: v for k, v in entry.items()
                 if k in known_fields and v not in (None, "")}
        # Don't keep `raw_score: 0` — scorer treats 0 as a real score, not a
        # missing value. Empty dict still gets a 0 from scorer, which is correct.
        out[dim_name] = clean

    return out, len(items)


def _sanitize_judge_output(data: dict, channel: str, skill_row=None) -> dict:
    """Coerce common LLM output structural mistakes back into the schema shape.

    Specifically handles:
    1. `weight_assignment = {"item": [{...}, ...]}` — LLM wrapped the per-dim
       entries in a single "item" key. Re-flatten using known-field detection
       + positional fallback to skill spec's dimension labels.
    2. `dimension_scores = {"item": [{...}, ...]}` — same wrap pattern; same
       unwrap. CRITICAL: without this, scorer sees only one non-dict key and
       `active_dimensions=0` → final_score = 0.
    3. Missing `dimension_scores` — LLM ran out of tokens. Default to `{}`.
    4. `root_causes` / `caps` / `skipped_dimensions` as parallel arrays.
    """
    if not isinstance(data, dict):
        return data

    # Pre-pass: resolve dimension names. WA's keys are preferred (they were
    # asked first and the LLM usually follows schema there). If WA was also
    # wrapped, fall back to the skill spec.
    n_dims_hint = 0
    wa_pre = data.get("weight_assignment")
    if isinstance(wa_pre, dict) and isinstance(wa_pre.get("item"), list):
        n_dims_hint = max(n_dims_hint, len(wa_pre["item"]))
    ds_pre = data.get("dimension_scores")
    if isinstance(ds_pre, dict) and isinstance(ds_pre.get("item"), list):
        n_dims_hint = max(n_dims_hint, len(ds_pre["item"]))

    if n_dims_hint > 0:
        dim_names = _resolve_dim_names(data, n_dims_hint, skill_row=skill_row)
    else:
        dim_names = []

    # 1) Unwrap weight_assignment.item
    wa = data.get("weight_assignment")
    if isinstance(wa, dict) and isinstance(wa.get("item"), list):
        flat, n = _unwrap_item_array(wa, _WEIGHT_FIELDS, dim_names)
        if n > 0:
            data["weight_assignment"] = flat
            _emit(channel, "step",
                  {"step": 1.5, "label": f"权重已从 {n} 维 unwrap"})

    # 2) Unwrap dimension_scores.item (THIS IS THE KEY FIX — without it,
    #    scorer sees `{"item": [...]}` and skips every dim → score=0)
    ds = data.get("dimension_scores")
    if isinstance(ds, dict) and isinstance(ds.get("item"), list):
        flat, n = _unwrap_item_array(ds, _DIM_SCORE_FIELDS, dim_names)
        if n > 0:
            data["dimension_scores"] = flat
            _emit(channel, "step",
                  {"step": 1.5, "label": f"维度评分已从 {n} 项 unwrap"})

    # 3) Default missing dimension_scores
    if not data.get("dimension_scores"):
        data["dimension_scores"] = {}
        _emit(channel, "step",
              {"step": 1.5, "label": "dimension_scores 缺失,已默认空(分数会归 0)"})

    # 4) root_causes / caps / skipped_dimensions as parallel arrays
    for field in ("root_causes", "caps", "skipped_dimensions"):
        v = data.get(field)
        if isinstance(v, dict):
            list_lengths = [
                len(x) for x in v.values()
                if isinstance(x, list) and x
            ]
            if len(list_lengths) >= 2 and len(set(list_lengths)) == 1:
                keys = list(v.keys())
                n = list_lengths[0]
                reshaped = []
                for i in range(n):
                    item = {}
                    for k in keys:
                        val = v[k]
                        if isinstance(val, list) and i < len(val):
                            item[k] = val[i]
                        else:
                            item[k] = val
                    reshaped.append(item)
                data[field] = reshaped
                _emit(channel, "step",
                      {"step": 1.5, "label": f"{field} 已从 {n} 条平行数组 unwrap"})
            elif not v:
                data[field] = []

    return data


def evaluate_batch(batch_id: str, run_ids: list[str]) -> None:
    """Run many evaluations concurrently (3 workers by default).

    Concurrency is bounded because LLM providers rate-limit per key. Set
    `EVAL_BATCH_CONCURRENCY` env var to tune. Each worker calls
    `evaluate_run()` which manages its own DB session, so SQLAlchemy
    session-sharing races don't apply.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    set_trace_id(f"batch-{batch_id[:6]}")
    channel = f"batches/{batch_id}"
    log.info("Batch %s: %d runs (concurrency=%d)",
             batch_id, len(run_ids), settings.eval_batch_concurrency)
    max_workers = max(1, min(settings.eval_batch_concurrency, len(run_ids) or 1))

    completed = 0
    if max_workers == 1:
        # Single-run batch — no point spinning a thread.
        for rid in run_ids:
            try:
                evaluate_run(rid)
            except Exception as exc:
                log.exception("Batch %s: run %s failed: %s", batch_id, rid, exc)
            completed += 1
            _emit(channel, "progress", {
                "index": completed, "total": len(run_ids), "run_id": rid,
            })
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_to_rid = {
                pool.submit(evaluate_run, rid): rid for rid in run_ids
            }
            for fut in as_completed(future_to_rid):
                rid = future_to_rid[fut]
                try:
                    fut.result()  # propagate inner exception via log
                except Exception as exc:
                    log.exception("Batch %s: run %s failed: %s",
                                  batch_id, rid, exc)
                completed += 1
                _emit(channel, "progress", {
                    "index": completed, "total": len(run_ids), "run_id": rid,
                })
    broker.close(channel)

    # ---- Persist to HF Datasets at the natural unit of work ----
    # Each run already calls mark_dirty() (see below); this triggers the actual
    # upload. Best-effort — a failed push just leaves the dirty flag set for
    # the periodic pusher / shutdown hook to retry.
    try:
        from .. import persistence
        persistence.push_db(reason=f"batch-end {batch_id[:8]}")
    except Exception as exc:  # pragma: no cover
        log.exception("HF push after batch failed (non-fatal): %s", exc)
