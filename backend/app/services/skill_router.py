"""Skill router: pick the right self-eval Skill for a given financial question.

Two stages:
- Stage A · keyword pre-filter (zero LLM cost)
- Stage B · LLM judgement (definitive, structured output)

Stage A is also the fallback when no LLM provider is available.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from ..utils.prompts import ROUTER_SYSTEM
from ..utils.trace import get_logger
from . import llm_client
from .skill_loader import get_loader

log = get_logger(__name__)


# ----------------------------------------------------------------------------
# Keyword dictionary derived from 自研评测Skill/README.md §3.2-3.3
# Each entry: skill code -> list of high-precision tokens
# ----------------------------------------------------------------------------
KEYWORDS: dict[str, list[str]] = {
    "01": ["事件", "政策", "地缘", "产业链", "概念股", "受益股", "对标", "题材", "炒作", "涨停板", "异动"],
    "02": ["回测", "计算", "统计", "涨跌幅", "概率", "复合条件", "区间", "区间涨跌", "区间收益"],
    "03": ["主力", "筹码", "止盈", "技术指标", "分红", "分时", "资金流", "增长点", "止盈位", "诊股", "诊断", "止损"],
    "04": ["能不能买", "为什么涨", "趋势", "估值", "投资价值", "走势解读", "K线解读"],
    "05": ["适合我", "推荐", "配置", "仓位", "解套", "加仓", "减仓", "持仓", "投顾", "建议"],
    "06": ["综合", "深度调研", "产业链全链", "多步推演", "全方位", "全面分析"],
    "07": ["错别字", "黑话", "追问", "上下文", "T+1", "北交所权限", "澄清", "请问您"],
    "08": ["政策", "新闻", "异动原因", "事件解读", "官媒", "公告", "解读", "为何", "为什么"],
    "09": ["年报", "季报", "财报", "业绩", "ROE", "毛利率", "会计差错", "净利润", "营收", "分红", "利润表"],
    "10": ["什么是", "术语", "定义", "规则", "集合竞价", "ST", "黑话", "概念是", "怎么算"],
    "11": ["为什么", "定义", "比较", "截止", "不要", "精简", "提炼", "改写", "优化"],
    "12": ["涨停", "潜力", "谁能追", "走势", "强势", "应该卖", "应该买", "卖掉", "形态"],
    "13": ["今天", "昨天", "明天", "下周", "交易日", "休市", "最新", "今日", "本周", "上周"],
}


# Skill weighting bumps based on edge-case clues (README §3.3)
EDGE_RULES: list[tuple[re.Pattern, dict[str, int]]] = [
    # Time-related override
    (re.compile(r"(今天|昨天|明天|下周|休市|交易日|最新).*(为何|是什么|大涨|大跌|消息)"),
     {"13": 5}),
    # KYC override on analysis
    (re.compile(r"(适合我|该不该|要不要|加仓|减仓|解套)"), {"05": 5}),
    # Compound intent: multi-clause questions
    (re.compile(r"[,，；;\n].{15,}.*?(并|同时|另外|此外|然后)"), {"06": 3}),
    # Instruction-following: explicit verbs
    (re.compile(r"^(请|帮我|帮忙)?(优化|改写|精简|提炼|总结|翻译)"), {"11": 5}),
    # Financial reasoning: 比较选哪个
    (re.compile(r"(.+)和(.+)(哪|哪个|哪只).*(卖|买|涨|跌|强|弱)"), {"12": 5}),
]


@dataclass
class RoutingResult:
    skill_code: str
    skill_id: str
    confidence: float
    reasoning: str
    alternatives: list[dict]
    stage_used: str  # keyword | llm | fallback | hint
    fallback: bool = False


# ============================================================================
def keyword_score(question: str) -> dict[str, int]:
    """Return per-skill keyword-hit score."""
    scores: dict[str, int] = {k: 0 for k in KEYWORDS}
    for code, kws in KEYWORDS.items():
        for kw in kws:
            if kw in question:
                scores[code] += 1
    for pat, bumps in EDGE_RULES:
        if pat.search(question):
            for code, delta in bumps.items():
                scores[code] = scores.get(code, 0) + delta
    return scores


def route(
    question: str,
    *,
    judge_model: Optional[str] = None,
    hint_skill_id: Optional[str] = None,
    use_llm: bool = True,
) -> RoutingResult:
    """Decide which Skill should evaluate this question."""
    loader = get_loader()
    self_skills = loader.scan_family("self")
    code_to_record = {r.code: r for r in self_skills}

    # 0. honour explicit hint
    if hint_skill_id and hint_skill_id in {r.id for r in self_skills}:
        rec = next(r for r in self_skills if r.id == hint_skill_id)
        return RoutingResult(
            skill_code=rec.code, skill_id=rec.id, confidence=1.0,
            reasoning="用户手动指定", alternatives=[], stage_used="hint",
        )

    scores = keyword_score(question)
    sorted_codes = sorted(scores.items(), key=lambda kv: -kv[1])
    top1_code, top1_score = sorted_codes[0]
    top1 = code_to_record.get(top1_code)

    # 1. LLM-based decision (preferred)
    if use_llm and judge_model is not None or use_llm and llm_client.list_models():
        try:
            return _llm_route(question, self_skills, judge_model)
        except Exception as exc:
            log.warning("LLM routing failed (%s), falling back to keywords", exc)

    # 2. Keyword fallback
    if not top1:
        # No skill records at all — should never happen if sync succeeded
        raise RuntimeError("No self-eval skills available; run sync_to_db() first")
    alternatives = [
        {"skill": code_to_record[c].name_zh, "skill_id": code_to_record[c].id,
         "why": f"keyword hits={s}"}
        for c, s in sorted_codes[1:4] if c in code_to_record and s > 0
    ]
    conf = min(0.6, 0.2 + top1_score * 0.08) if top1_score else 0.15
    return RoutingResult(
        skill_code=top1.code, skill_id=top1.id, confidence=conf,
        reasoning=f"关键词命中 {top1_score} (top-1)",
        alternatives=alternatives,
        stage_used="keyword" if llm_client.list_models() else "fallback",
        fallback=not llm_client.list_models(),
    )


def _llm_route(question: str, self_skills, judge_model: Optional[str]) -> RoutingResult:
    """Use an LLM to confirm the routing decision."""
    skills_brief = "\n".join(
        f"- {r.code} · {r.name_zh}: {r.one_liner or r.description[:120]}"
        for r in self_skills
    )
    system = ROUTER_SYSTEM.format(skills_brief=skills_brief)
    code_options = sorted([r.code for r in self_skills])

    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["predicted_skill_code", "confidence", "reasoning"],
        "properties": {
            "predicted_skill_code": {"type": "string", "enum": code_options},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "reasoning": {"type": "string", "minLength": 4, "maxLength": 800},
            "alternatives": {
                "type": "array",
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["skill_code", "why"],
                    "properties": {
                        "skill_code": {"type": "string", "enum": code_options},
                        "why": {"type": "string", "maxLength": 200},
                    },
                },
            },
        },
    }
    result = llm_client.call_with_schema(
        model_id=judge_model,
        system=system,
        user={"question": question},
        schema=schema,
        tool_name="submit_routing",
        max_tokens=512,
        temperature=0.1,
    )
    data = result.data
    code = data["predicted_skill_code"]
    rec = next((r for r in self_skills if r.code == code), None)
    if rec is None:
        raise RuntimeError(f"LLM returned unknown skill code {code}")

    code_to_rec = {r.code: r for r in self_skills}
    alts = []
    for alt in data.get("alternatives", []) or []:
        ar = code_to_rec.get(alt["skill_code"])
        if ar:
            alts.append({"skill": ar.name_zh, "skill_id": ar.id, "why": alt["why"]})

    return RoutingResult(
        skill_code=code, skill_id=rec.id,
        confidence=float(data["confidence"]),
        reasoning=data["reasoning"],
        alternatives=alts,
        stage_used="llm",
    )
