"""Pure-Python tests for the scoring helpers — no DB or LLM needed."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.scorer import compute_scores, pass_threshold, top_root_cause


def test_basic_weighted_sum():
    weights = {
        "a": {"dynamic_weight": 60, "applicability": "relevant"},
        "b": {"dynamic_weight": 40, "applicability": "relevant"},
    }
    dims = {
        "a": {"raw_score": 80},
        "b": {"raw_score": 60},
    }
    r = compute_scores(weights, dims, [])
    # 60% * 80 + 40% * 60 = 48 + 24 = 72
    assert abs(r.absolute_score_pre_cap - 72.0) < 0.01, r
    assert abs(r.final_score - 72.0) < 0.01
    assert r.warnings == []
    assert r.active_dimensions == 2
    assert r.weights_sum == 100


def test_cap_applied_only_when_below_weighted():
    weights = {"a": {"dynamic_weight": 100, "applicability": "relevant"}}
    dims = {"a": {"raw_score": 80}}
    caps = [{"rule_id": "x", "triggered": True, "score_ceiling": 60}]
    r = compute_scores(weights, dims, caps)
    assert r.absolute_score_pre_cap == 80.0
    assert r.final_score == 60.0


def test_multiple_caps_take_lowest():
    weights = {"a": {"dynamic_weight": 100, "applicability": "relevant"}}
    dims = {"a": {"raw_score": 100}}
    caps = [
        {"rule_id": "x", "triggered": True, "score_ceiling": 65},
        {"rule_id": "y", "triggered": True, "score_ceiling": 35},
        {"rule_id": "z", "triggered": False, "score_ceiling": 20},
    ]
    r = compute_scores(weights, dims, caps)
    assert r.final_score == 35.0
    assert len(r.triggered_caps) == 2


def test_not_applicable_skipped():
    weights = {
        "a": {"dynamic_weight": 50, "applicability": "relevant"},
        "b": {"dynamic_weight": 50, "applicability": "relevant"},
        "c": {"dynamic_weight": 0, "applicability": "not_applicable"},
    }
    dims = {
        "a": {"raw_score": 80},
        "b": {"raw_score": 80},
        "c": {"raw_score": 0},
    }
    r = compute_scores(weights, dims, [])
    assert r.active_dimensions == 2
    assert r.final_score == 80.0


def test_weights_not_summing_to_100_warns():
    weights = {
        "a": {"dynamic_weight": 60, "applicability": "relevant"},
        "b": {"dynamic_weight": 30, "applicability": "relevant"},
    }
    dims = {"a": {"raw_score": 100}, "b": {"raw_score": 100}}
    r = compute_scores(weights, dims, [])
    assert any("90" in w for w in r.warnings)


def test_six_grade_violation_warns_but_keeps_value():
    weights = {"a": {"dynamic_weight": 100, "applicability": "relevant"}}
    dims = {"a": {"raw_score": 73}}  # not a six-grade value
    r = compute_scores(weights, dims, [])
    assert any("非六档分" in w for w in r.warnings)
    assert r.final_score == 73.0  # value still used


def test_top_root_cause_picks_lowest_score():
    rcs = [
        {"l1": "intent", "raw_score": 60},
        {"l1": "evidence", "raw_score": 20},
        {"l1": "tool", "raw_score": 80},
    ]
    l1, _ = top_root_cause(rcs)
    assert l1 == "evidence"


def test_pass_threshold():
    assert pass_threshold(60) is True
    assert pass_threshold(59.99) is False
    assert pass_threshold(None) is None
