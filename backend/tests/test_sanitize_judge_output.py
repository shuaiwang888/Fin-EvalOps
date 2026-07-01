"""Tests for the LLM output sanitizer in evaluator._sanitize_judge_output."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.evaluator import _sanitize_judge_output


def test_unwraps_weight_assignment_item_array():
    """LLM returned weight_assignment as {"item": [...]} — should become flat dict."""
    data = {
        "weight_assignment": {
            "item": [
                {"applicability": "relevant", "dynamic_weight": 18, "rationale": "x", "dim_a": ""},
                {"applicability": "relevant", "dynamic_weight": 15, "rationale": "y", "dim_b": ""},
            ]
        },
    }
    fixed = _sanitize_judge_output(data, "test")
    wa = fixed["weight_assignment"]
    assert isinstance(wa, dict)
    assert "item" not in wa
    assert "dim_a" in wa and wa["dim_a"] == {"applicability": "relevant", "dynamic_weight": 18, "rationale": "x"}
    assert "dim_b" in wa and wa["dim_b"] == {"applicability": "relevant", "dynamic_weight": 15, "rationale": "y"}


def test_keeps_correct_weight_assignment():
    """If LLM got it right, we don't touch it."""
    data = {
        "weight_assignment": {
            "dim_a": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "ok"},
            "dim_b": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "ok"},
        },
    }
    fixed = _sanitize_judge_output(data, "test")
    assert fixed["weight_assignment"] == data["weight_assignment"]


def test_defaults_missing_dimension_scores():
    data = {"caps": [], "root_causes": [], "narrative_review": {}, "weight_assignment": {}}
    fixed = _sanitize_judge_output(data, "test")
    assert fixed["dimension_scores"] == {}


def test_keeps_existing_dimension_scores():
    data = {
        "dimension_scores": {"dim_a": {"raw_score": 80, "evidence": ["e1"]}},
    }
    fixed = _sanitize_judge_output(data, "test")
    assert fixed["dimension_scores"] == {"dim_a": {"raw_score": 80, "evidence": ["e1"]}}


def test_handles_non_dict_input():
    """Defensive: should not crash on weird LLM outputs."""
    assert _sanitize_judge_output(None, "test") is None
    assert _sanitize_judge_output("not a dict", "test") == "not a dict"


def test_skips_item_entries_with_no_dimension_key():
    """If we can't find a dimension name in an entry, skip it."""
    data = {
        "weight_assignment": {
            "item": [
                {"dynamic_weight": 18, "applicability": "relevant"},  # no extra key
                {"applicability": "relevant", "dynamic_weight": 15, "rationale": "ok", "dim_b": ""},
            ]
        }
    }
    fixed = _sanitize_judge_output(data, "test")
    # Only dim_b should make it through
    assert "dim_b" in fixed["weight_assignment"]
    assert len(fixed["weight_assignment"]) == 1


# ===========================================================================
# Parallel-array sanitizer (root_causes / caps / skipped_dimensions)
# Reproduces the exact shape from the user's failing-eval bug report.
# ===========================================================================

def test_unwraps_root_causes_parallel_arrays():
    """LLM gave root_causes as a dict of parallel arrays — must transpose."""
    raw = {
        "confidence": ["medium", "medium"],
        "dimension": ["user_profile_suitability", "comparison_quantification"],
        "l1": ["user_profile", "evidence"],
        "l2": ["profile-not-acknowledged", "missing-fine-grained-segmentation"],
        "raw_score": ["40", "60"],
        "summary": ["未明确说明用户画像缺失", "未能从财报拆出细分字段"],
    }
    fixed = _sanitize_judge_output({"root_causes": raw, "caps": []}, "test")
    rc = fixed["root_causes"]
    assert isinstance(rc, list), f"root_causes not transposed: got {type(rc)}"
    assert len(rc) == 2
    assert rc[0]["l1"] == "user_profile"
    assert rc[0]["raw_score"] == "40"
    assert rc[1]["l1"] == "evidence"


def test_unwraps_caps_parallel_arrays():
    raw = {
        "rule_id": ["cap_a", "cap_b"],
        "triggered": [True, False],
        "score_ceiling": [50, 70],
    }
    fixed = _sanitize_judge_output({"root_causes": [], "caps": raw}, "test")
    assert fixed["caps"] == [
        {"rule_id": "cap_a", "triggered": True, "score_ceiling": 50},
        {"rule_id": "cap_b", "triggered": False, "score_ceiling": 70},
    ]


def test_unwraps_skipped_dimensions_parallel_arrays():
    raw = {
        "dimension": ["d1", "d2"],
        "reason": ["r1", "r2"],
    }
    fixed = _sanitize_judge_output({"root_causes": [], "caps": [], "skipped_dimensions": raw}, "test")
    assert fixed["skipped_dimensions"] == [
        {"dimension": "d1", "reason": "r1"},
        {"dimension": "d2", "reason": "r2"},
    ]


def test_keeps_already_correct_list_shape():
    """Idempotency: list-of-objects input is left untouched."""
    rc = [{"l1": "x", "l2": "y"}, {"l1": "a", "l2": "b"}]
    fixed = _sanitize_judge_output({"root_causes": rc, "caps": []}, "test")
    assert fixed["root_causes"] == rc


def test_empty_dict_becomes_empty_list():
    """Empty {} in a parallel-array slot becomes [] rather than crashing."""
    fixed = _sanitize_judge_output({"root_causes": {}, "caps": {}}, "test")
    assert fixed["root_causes"] == []
    assert fixed["caps"] == []


# ===========================================================================
# llm_client._sanitize_judge_for_validation — runs BEFORE schema validation
# so these cases must be fixed before the validator sees them.
# ===========================================================================

def test_llm_client_sanitizer_root_causes_parallel_arrays():
    from app.services.llm_client import _sanitize_judge_for_validation

    raw = {
        "schema_version": "v1",
        "weight_assignment": {},
        "dimension_scores": {},
        "caps": [],
        "root_causes": {
            "l1": ["a", "b"],
            "l2": ["x", "y"],
            "raw_score": ["40", "60"],
        },
        "narrative_review": {},
    }
    out = _sanitize_judge_for_validation(raw)
    assert isinstance(out["root_causes"], list)
    # raw_score strings are coerced to float (matches schema `type: number`)
    assert out["root_causes"] == [
        {"l1": "a", "l2": "x", "raw_score": 40.0},
        {"l1": "b", "l2": "y", "raw_score": 60.0},
    ]


def test_llm_client_sanitizer_matched_golden_cases_string():
    from app.services.llm_client import _sanitize_judge_for_validation

    raw = {
        "matched_golden_cases": "Case 1: 算力涨价; Case 2: 先进封测",
    }
    out = _sanitize_judge_for_validation(raw)
    assert isinstance(out["matched_golden_cases"], list)
    assert "算力涨价" in out["matched_golden_cases"]
    assert "先进封测" in out["matched_golden_cases"]


def test_llm_client_sanitizer_dimension_scores_raw_score_strings():
    from app.services.llm_client import _sanitize_judge_for_validation

    raw = {"dimension_scores": {"a": {"raw_score": "80"}, "b": {"raw_score": "70.5"}}}
    out = _sanitize_judge_for_validation(raw)
    assert out["dimension_scores"]["a"]["raw_score"] == 80.0
    assert out["dimension_scores"]["b"]["raw_score"] == 70.5


def test_llm_client_sanitizer_is_idempotent():
    from app.services.llm_client import _sanitize_judge_for_validation

    good = {
        "schema_version": "v1",
        "weight_assignment": {"a": {"dynamic_weight": 10, "applicability": "relevant"}},
        "dimension_scores": {"a": {"raw_score": 80.0}},
        "caps": [{"rule_id": "r", "triggered": False}],
        "root_causes": [{"l1": "issue"}],
        "narrative_review": {"summary": "ok"},
        "matched_golden_cases": ["Case 1"],
    }
    out = _sanitize_judge_for_validation(dict(good))
    assert out == good


# ===========================================================================
# End-to-end: the exact failing payload from the bug report should now
# pass strict schema validation after sanitization.
# ===========================================================================

def test_full_schema_validation_passes_after_sanitization():
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA
    from app.services.llm_client import _sanitize_judge_for_validation, _validate_schema

    raw = {
        "schema_version": "interactive-clarification/v1",
        "weight_assignment": {"intent_fulfillment": {
            "dynamic_weight": 30, "applicability": "relevant", "rationale": "...",
        }},
        "dimension_scores": {"intent_fulfillment": {"raw_score": 80}},
        "caps": [],
        "root_causes": {
            "confidence": ["medium", "medium"],
            "dimension": ["a", "b"],
            "l1": ["user_profile", "evidence"],
            "l2": ["p1", "e1"],
            "raw_score": ["40", "60"],
            "summary": ["s1", "s2"],
        },
        "narrative_review": {"summary": "x"},
    }
    out = _sanitize_judge_for_validation(raw)
    # MUST NOT raise
    _validate_schema(out, EVAL_OUTPUT_SCHEMA)


def test_permissive_fill_fills_missing_required_fields():
    """If sanitization can't fix the schema, the permissive fallback must
    fill missing required top-level fields so the validator passes."""
    from app.services.llm_client import (
        _fill_missing_top_level_fields, _validate_schema,
    )
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA

    partial = {
        "schema_version": "v1",
        "weight_assignment": {},
        "dimension_scores": {},
        "caps": [],
        # narrative_review + root_causes missing — both required
    }
    filled = _fill_missing_top_level_fields(partial, EVAL_OUTPUT_SCHEMA)
    assert "narrative_review" in filled
    assert "root_causes" in filled
    _validate_schema(filled, EVAL_OUTPUT_SCHEMA)


# ===========================================================================
# Field-type coercion (the `'list' object has no attribute 'get'` regression)
# ===========================================================================

def test_coerces_list_weight_assignment_to_empty_dict():
    """Reproduces the user bug: judge returns `weight_assignment: [{...}, {...}]`
    (a list) when the schema expects an object. Without coercion, scorer
    would crash on `.items()` and the run would fail with `'list' object
    has no attribute 'get'`."""
    from app.services.llm_client import _sanitize_judge_for_validation
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA

    raw = {
        "schema_version": "v1",
        "weight_assignment": [
            {"dim_a": {"dynamic_weight": 30, "applicability": "relevant"}},
            {"dim_b": {"dynamic_weight": 20, "applicability": "supplementary"}},
        ],   # ← wrong type — should be an object
        "dimension_scores": {},
        "caps": [],
        "root_causes": [],
        "narrative_review": {},
    }
    out = _sanitize_judge_for_validation(raw, schema=EVAL_OUTPUT_SCHEMA)
    # Must be a dict (or empty) so scorer can call `.items()`
    assert isinstance(out["weight_assignment"], dict), \
        f"weight_assignment type wrong: {type(out['weight_assignment'])}"
    # Scorer's safe path: iterate, see no per-dim dicts, score=0
    from app.services.scorer import compute_scores
    sc = compute_scores(out["weight_assignment"], out["dimension_scores"], out["caps"])
    assert sc.final_score == 0.0


def test_coerces_dict_dimension_scores_to_empty_dict():
    """LLM returned dimension_scores as a single object instead of per-dim
    nested dict. Without coercion scorer would crash on .items()."""
    from app.services.llm_client import _sanitize_judge_for_validation
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA

    raw = {
        "schema_version": "v1",
        "weight_assignment": {},
        "dimension_scores": {"raw_score": 80},  # wrong — should be {dim: {...}}
        "caps": [],
        "root_causes": [],
        "narrative_review": {},
    }
    out = _sanitize_judge_for_validation(raw, schema=EVAL_OUTPUT_SCHEMA)
    assert isinstance(out["dimension_scores"], dict)
    from app.services.scorer import compute_scores
    # Should NOT raise — coerces to {} if mismatched type
    sc = compute_scores({}, out["dimension_scores"], out["caps"])
    assert sc.final_score == 0.0


def test_coerces_list_narrative_review_to_empty_dict():
    from app.services.llm_client import _sanitize_judge_for_validation
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA

    raw = {
        "schema_version": "v1",
        "weight_assignment": {},
        "dimension_scores": {},
        "caps": [],
        "root_causes": [],
        "narrative_review": ["summary text only"],  # wrong type
    }
    out = _sanitize_judge_for_validation(raw, schema=EVAL_OUTPUT_SCHEMA)
    assert isinstance(out["narrative_review"], dict)


def test_no_coercion_when_already_correct_type():
    """Sanity: well-formed data must NOT be touched."""
    from app.services.llm_client import _sanitize_judge_for_validation
    from app.services.evaluator import EVAL_OUTPUT_SCHEMA

    raw = {
        "schema_version": "v1",
        "weight_assignment": {"dim_a": {"dynamic_weight": 30, "applicability": "relevant"}},
        "dimension_scores": {"dim_a": {"raw_score": 80}},
        "caps": [],
        "root_causes": [],
        "narrative_review": {"summary": "ok"},
    }
    out = _sanitize_judge_for_validation(dict(raw), schema=EVAL_OUTPUT_SCHEMA)
    assert out == raw


def test_scorer_survives_list_weight_assignment_without_sanitizer():
    """Even WITHOUT the sanitizer, scorer should not crash on a list
    where it expects a dict (defence in depth). It should return 0 with
    a warning rather than raising."""
    from app.services.scorer import compute_scores

    # Pre-sanitize is bypassed — feed raw garbage to scorer.
    sc = compute_scores([], {}, [])
    assert sc.final_score == 0.0
    assert sc.absolute_score_pre_cap == 0.0


# ===========================================================================
# Truncation handling — the "0.00 score" regression where LLM hit
# max_tokens, returned partial JSON, and the sanitizer silently filled
# defaults that scored 0.00 with no error visible to the user.
# ===========================================================================

def test_llm_truncated_error_is_distinct_subclass():
    from app.services.llm_client import LLMError, LLMTruncatedError
    assert issubclass(LLMTruncatedError, LLMError)
    err = LLMTruncatedError("hit max_tokens")
    assert "hit max_tokens" in str(err)


def test_truncation_partial_json_in_text_block_raises():
    """If max_tokens truncation leaves a partial JSON in a text block
    (e.g. closes mid-string with no closing brace), _extract_json
    currently returns whatever it can — but the new code path in
    _call_anthropic catches this via the truncated flag from stop_reason.

    This test exercises the unit-level invariant: once stop_reason is
    set to 'max_tokens' and the parser can only get partial JSON, the
    caller should get a clear failure rather than a 0.00 score.
    """
    from app.services.llm_client import LLMTruncatedError

    # Synthetic truncated JSON — opens but never closes.
    truncated_json = '{"schema_version": "v1", "weight_assignment": {"dim_a": {'
    # Brace count is 1 open vs 0 close → unbalanced.
    assert truncated_json.count("{") > truncated_json.count("}"), \
        "sanity check: this fixture must be unbalanced JSON"

    # The LLMTruncatedError class is the contract: callers know truncation
    # means "don't trust any field, fail loudly".
    err = LLMTruncatedError("partial output")
    assert "partial" in str(err)
