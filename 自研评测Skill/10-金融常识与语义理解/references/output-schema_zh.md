# 输出格式规范

先输出结构化 JSON。需要可读摘要时，在 JSON 后附简短自然语言评审。

```json
{
  "schema_version": "financial-common-sense-and-semantic-understanding/v3",
  "weight_assignment": {
    "semantic_intent_alignment": {"dynamic_weight": 25, "applicability": "relevant", "rationale": "题目依赖真实意图识别"},
    "financial_term_understanding": {"dynamic_weight": 25, "applicability": "relevant", "rationale": "需要理解金融术语或交易规则"},
    "entity_product_boundary": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "涉及产品或实体边界"},
    "metric_caliber_accuracy": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "涉及指标公式、披露期或数据口径"},
    "credibility_expression": {"dynamic_weight": 10, "applicability": "supplementary", "rationale": "需解释清楚并避免空泛"},
    "tool_usage": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需核验工具和数据来源是否匹配"}
  },
  "skipped_dimensions": ["timeliness_context"],
  "matched_golden_cases": [
    {
      "case_id": "case_10_pe_negative",
      "matched_reason": "用户要求 PE 最小，语义匹配负 PE 处理案例",
      "hard_checks_used": ["不得把负 PE 直接当作估值最小的优质结果"]
    }
  ],
  "dimension_scores": {
    "semantic_intent_alignment": {"raw_score": 0, "evidence": []},
    "financial_term_understanding": {"raw_score": 0, "evidence": []},
    "entity_product_boundary": {"raw_score": 0, "evidence": []},
    "metric_caliber_accuracy": {"raw_score": 0, "evidence": []},
    "credibility_expression": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "hard_concept_or_rule_error",
      "triggered": false,
      "score_ceiling": 40,
      "reason": "",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "intent",
      "l2": "semantic-target-misread",
      "dimension": "semantic_intent_alignment",
      "raw_score": 20,
      "confidence": "high",
      "summary": "答案把用户真实对象理解错，导致后续口径和结论偏离。",
      "evidence": []
    }
  ],
  "narrative_review": {
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "next_actions": []
  }
}
```

## 证据对象

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短证据摘要"
}
```

字段规则：
- `schema_version` 固定为 `financial-common-sense-and-semantic-understanding/v3`。
- `dynamic_weight` 总和必须为 100。
- `dimension_scores` 只包含 `relevant` 和 `supplementary` 维度（`not_applicable` 维度不出现在 `dimension_scores` 和 `weight_assignment` 中）。
- `raw_score` 只取 0/20/40/60/80/100 六档整数。
- 不输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`，这些由调用方代码计算。
