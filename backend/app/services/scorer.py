"""Scorer — applies weights and caps to raw judge output.

Inputs come from the evaluator's structured JSON response:
- weight_assignment: {dim_key: {dynamic_weight, applicability, ...}}
- dimension_scores: {dim_key: {raw_score, evidence, ...}}
- caps: [{rule_id, triggered, score_ceiling, ...}]

Outputs added to the Run row:
- absolute_score_pre_cap: weighted sum
- final_score: pre-cap clamped by min of triggered ceilings
- warnings: list of validation issues
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from ..utils.trace import get_logger

log = get_logger(__name__)


@dataclass
class ScoringResult:
    absolute_score_pre_cap: float
    final_score: float
    weights_sum: int
    triggered_caps: List[dict]
    warnings: List[str]
    active_dimensions: int


def compute_scores(
    weight_assignment: Optional[Dict[str, Any]],
    dimension_scores: Optional[Dict[str, Any]],
    caps: Optional[List[Dict[str, Any]]],
) -> ScoringResult:
    warnings: list[str] = []
    weights = weight_assignment or {}
    dims = dimension_scores or {}
    caps = caps or []

    # weights total
    total_weight = 0
    for k, v in weights.items():
        if not isinstance(v, dict):
            continue
        try:
            w = int(v.get("dynamic_weight", 0) or 0)
        except (TypeError, ValueError):
            w = 0
        applicability = (v.get("applicability") or "").lower()
        if applicability != "not_applicable":
            total_weight += w
    if total_weight != 100:
        warnings.append(f"weight_assignment 总和={total_weight} ≠ 100")

    # weighted sum across active dimensions
    weighted = 0.0
    active = 0
    for dim_key, dim_v in dims.items():
        if not isinstance(dim_v, dict):
            continue
        try:
            raw = float(dim_v.get("raw_score", 0) or 0)
        except (TypeError, ValueError):
            raw = 0.0
        if raw < 0 or raw > 100:
            warnings.append(f"维度 {dim_key} raw_score 越界:{raw}")
            raw = max(0.0, min(100.0, raw))
        # six-grade enforcement
        if raw not in {0, 20, 40, 60, 80, 100}:
            warnings.append(f"维度 {dim_key} raw_score={raw} 非六档分,已保留原值")
        w_entry = weights.get(dim_key) or {}
        applicability = (w_entry.get("applicability") or "relevant").lower()
        if applicability == "not_applicable":
            continue
        try:
            dyn_w = float(w_entry.get("dynamic_weight", 0) or 0)
        except (TypeError, ValueError):
            dyn_w = 0.0
        weighted += raw / 100.0 * dyn_w
        active += 1

    triggered_caps = [c for c in caps if isinstance(c, dict) and c.get("triggered")]
    ceiling = None
    for c in triggered_caps:
        try:
            ceil = float(c.get("score_ceiling", 100))
        except (TypeError, ValueError):
            ceil = 100.0
        ceiling = ceil if ceiling is None else min(ceiling, ceil)

    final = weighted if ceiling is None else min(weighted, ceiling)

    return ScoringResult(
        absolute_score_pre_cap=round(weighted, 2),
        final_score=round(final, 2),
        weights_sum=total_weight,
        triggered_caps=triggered_caps,
        warnings=warnings,
        active_dimensions=active,
    )


def pass_threshold(score: Optional[float], threshold: float = 60.0) -> Optional[bool]:
    if score is None:
        return None
    return score >= threshold


def top_root_cause(root_causes: Optional[List[Dict[str, Any]]]) -> Tuple[Optional[str], Optional[str]]:
    """Return (L1, L2) of the highest-impact root cause (= lowest raw_score)."""
    if not root_causes:
        return None, None
    candidates = []
    for rc in root_causes:
        if not isinstance(rc, dict):
            continue
        try:
            score = float(rc.get("raw_score", 100))
        except (TypeError, ValueError):
            score = 100.0
        candidates.append((score, rc))
    if not candidates:
        return None, None
    candidates.sort(key=lambda kv: kv[0])
    best = candidates[0][1]
    return best.get("l1"), best.get("l2")
