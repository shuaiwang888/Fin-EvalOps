# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "consultation-and-qa/v1",
  "weight_assignment": {
    "intent_fulfillment": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "用户要求解释事件影响并给出判断"},
    "timeliness_fact_boundary": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "问题包含最新/近期/截至某日"},
    "fact_evidence_quality": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需要可靠事实、数据口径和来源"},
    "information_integration": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需要整合政策、监管、产业和公司事件"},
    "investment_mapping": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "用户关心对行业和标的的影响"},
    "core_signal_extraction": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需要抓住主要催化剂而非素材罗列"},
    "nonstandard_source_awareness": {"dynamic_weight": 8, "applicability": "supplementary", "rationale": "问题可能涉及市场传闻、调研纪要或大V文章"},
    "credibility_expression": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达可信度始终有参考价值"},
    "tool_usage": {"dynamic_weight": 8, "applicability": "relevant", "rationale": "资讯问答依赖检索与交叉验证策略"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "case_06_recent_pharma_two_weeks",
      "matched_reason": "用户要求近两周医药政策资讯，需严格时间窗口和政策层级梳理",
      "hard_checks_used": ["落实近两周时间窗口", "按政策/监管/企业事件组织", "给出创新支持与合规收紧的主导判断"]
    }
  ],
  "dimension_scores": {
    "intent_fulfillment": {"raw_score": 60, "evidence": []},
    "timeliness_fact_boundary": {"raw_score": 40, "evidence": []},
    "fact_evidence_quality": {"raw_score": 60, "evidence": []},
    "information_integration": {"raw_score": 60, "evidence": []},
    "investment_mapping": {"raw_score": 40, "evidence": []},
    "core_signal_extraction": {"raw_score": 40, "evidence": []},
    "nonstandard_source_awareness": {"raw_score": 60, "evidence": []},
    "credibility_expression": {"raw_score": 60, "evidence": []},
    "tool_usage": {"raw_score": 40, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "hard_time_or_fact_error",
      "triggered": false,
      "score_ceiling": 40,
      "reason": "",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "evidence",
      "l2": "time_window_not_enforced",
      "dimension": "timeliness_fact_boundary",
      "raw_score": 40,
      "confidence": "high",
      "summary": "答案没有把用户要求的近期时间窗口落到具体事件和日期上。",
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

## 证据对象格式

```json
{
  "source": "question | final_answer | answer | context | reasoning | function_call | function_call_output",
  "pointer": "question | text_answer | answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短证据摘要"
}
```

评分以 `text_answer` 为主锚点。只有在检查图表、截图、链接或 markdown 呈现时才引用 `answer`。

## 字段规则

- `schema_version` 固定为 `consultation-and-qa/v1`。
- `weight_assignment` 必须包含所有维度，`dynamic_weight` 总和必须等于 100。
- `skipped_dimensions` 只放 `not_applicable` 维度。
- `matched_golden_cases` 记录命中的专家案例、图像锚点和实际使用的 hard checks；未命中时为空数组。
- `dimension_scores` 只包含活跃维度，每个维度只输出 `raw_score` 和 `evidence`。
- `caps` 至少包含所有触发的封顶规则；未触发但关键检查过的规则也可保留。
- `root_causes` 按重要程度排序。除非所有活跃维度均不低于 80 且无封顶触发，否则至少输出一个根因。
- `narrative_review` 保持短小，重点说明主要问题和可执行修复建议。

