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
