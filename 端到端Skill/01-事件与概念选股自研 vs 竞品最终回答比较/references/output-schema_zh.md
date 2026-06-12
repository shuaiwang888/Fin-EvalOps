# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "event-concept-stock-selection-self-vs-competitor-result-only/v1",
  "pairing": {
    "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "answer_anchors": {
    "self_final_answer_pointer": "",
    "competitor_final_answer_pointer": ""
  },
  "weight_assignment": {
    "intent_fulfillment": {"dynamic_weight": 22, "applicability": "relevant", "rationale": ""},
    "event_abstraction": {"dynamic_weight": 16, "applicability": "relevant", "rationale": ""},
    "industry_mapping": {"dynamic_weight": 14, "applicability": "relevant", "rationale": ""},
    "ranking_judgment": {"dynamic_weight": 16, "applicability": "relevant", "rationale": ""},
    "logic_closure": {"dynamic_weight": 17, "applicability": "relevant", "rationale": ""},
    "timeliness_fact_boundary": {"dynamic_weight": 10, "applicability": "supplementary", "rationale": ""},
    "credibility_expression": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": ""}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "self_evaluation": {
    "dimension_scores": {
      "intent_fulfillment": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "event_abstraction": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "industry_mapping": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "ranking_judgment": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "logic_closure": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "timeliness_fact_boundary": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "credibility_expression": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []}
    },
    "absolute_score_pre_cap": 0,
    "applied_caps": [],
    "final_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": []
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "intent_fulfillment": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "event_abstraction": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "industry_mapping": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "ranking_judgment": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "logic_closure": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "timeliness_fact_boundary": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []},
      "credibility_expression": {"raw_score": 0, "dynamic_weight": 0, "rationale": "", "evidence": []}
    },
    "absolute_score_pre_cap": 0,
    "applied_caps": [],
    "final_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": []
  },
  "dimension_comparison": {
    "intent_fulfillment": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    }
  },
  "self_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "self_weaknesses": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "competitor_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "shared_failures": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "comparison_summary": {
    "absolute_summary": "",
    "relative_summary": "",
    "verdict": "self_better | competitor_better | tie | both_poor",
    "self_final_score": 0,
    "competitor_final_score": 0,
    "score_delta": 0,
    "why": []
  }
}
```

## 字段规则

- `schema_version`：固定为 `event-concept-stock-selection-self-vs-competitor-result-only/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识。
- `pairing.self_model_id`：固定为 `"self"`，除非调用方提供明确自研模型名。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `answer_anchors`：记录双方最终回答实际读取位置。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致，权重总和必须为 100。
- `skipped_dimensions`：仅当维度完全不适用于本题时加入。
- `matched_golden_cases`：命中的专家案例 ID 列表；不命中时留空。
- `dimension_scores`：每个活跃维度必须包含 `raw_score`、`dynamic_weight`、`rationale`、`evidence`（`weighted_score` 由评测引擎注入，LLM 无需输出）。
- `absolute_score_pre_cap`：由评测引擎根据活跃维度的 raw_score 和 dynamic_weight 自动计算。
- `applied_caps`：记录触发的封顶标签。本类别沿用标签式封顶：`applied_caps` 不直接改写分数。
- `final_score`：由评测引擎根据 `absolute_score_pre_cap` 和 `applied_caps` 自动计算。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据；`score_delta = self_raw_score - competitor_raw_score`。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品最终回答中真正值得学习的地方。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `comparison_summary.verdict`：若双方都明显不达标，即便一方分数略高，也应使用 `both_poor`。

## 证据对象格式

```json
{
  "source": "question | self_final_answer | competitor_final_answer",
  "pointer": "question | self_record.text_answer | self_record.answer | competitor_record.text_answer | competitor_record.answer | normalized.self_final_answer | normalized.competitor_final_answer",
  "quote_or_summary": "",
  "rationale": ""
}
```

## 证据使用原则

- 每个维度评分至少一条 evidence。
- 每条 `self_strengths`、`self_weaknesses`、`competitor_strengths`、`shared_failures` 至少一条 evidence。
- evidence 只能指向用户问题、自研最终回答或竞品最终回答。
- `quote_or_summary` 优先使用短原文；原文过长时可以摘要，但必须通过 pointer 回指。
- 如果最终回答没有体现某个信息，不能把它写成评分依据、优点、缺点、共同失败点或胜负原因。

封顶规则在本类别中作为标签保留，不修改 `final_score`。如后续类别改为硬封顶，应在该类别 schema 中明确 `final_score = min(absolute_score_pre_cap, lowest_ceiling)`。
