"""Tests for the keyword-based stage of skill_router.

These do not require any LLM provider — they exercise the rule-based
predicate that's also our fallback path.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.skill_router import keyword_score


def _top(question: str) -> str:
    s = keyword_score(question)
    return max(s.items(), key=lambda kv: kv[1])[0]


def test_time_awareness_question():
    assert _top("今天晶瑞电材大跌-8%是什么利空消息吗") == "13"


def test_kyc_question():
    assert _top("东方雨虹当前适合加仓还是减仓？") == "05"


def test_financial_reasoning_compare():
    assert _top("从技术形态看,三安光电和三星电气哪支股票应该卖掉") == "12"


def test_instruction_following():
    assert _top("帮我优化以下平安证券资管部介绍,重点突出优势") == "11"


def test_financial_report_interpretation():
    # 财报关键词应该提示 09 / 02
    s = keyword_score("百普赛斯的净利润增长是否可持续？")
    assert s["09"] > 0
