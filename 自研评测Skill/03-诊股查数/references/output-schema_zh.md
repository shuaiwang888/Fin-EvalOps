# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短的自然语言评审。

## JSON 结构

```json
{
  "schema_version": "stock-diagnosis-data-lookup/v1",
  "weight_assignment": {
    "intent_fulfillment": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "用户要求诊断主力是否进场"},
    "data_accuracy_coverage": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "需要资金流和龙虎榜等事实数据"},
    "time_caliber_precision": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "问题指定4月10日"},
    "calculation_comparison": {"dynamic_weight": 0, "applicability": "not_applicable", "rationale": "无明确计算或多标的对比"},
    "analysis_framework_fit": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "主力有大资金和游资两层含义"},
    "insight_extension": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需判断资金行为对个股的含义"},
    "result_verifiability": {"dynamic_weight": 8, "applicability": "supplementary", "rationale": "列出明细可帮助核验"},
    "presentation_visualization": {"dynamic_weight": 3, "applicability": "supplementary", "rationale": "表达清晰有参考价值"},
    "tool_usage": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需检查资金数据与龙虎榜查询"},
    "latency_efficiency": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "有耗时证据但不是核心质量"}
  },
  "skipped_dimensions": ["calculation_comparison"],
  "matched_golden_cases": [
    {
      "case_id": "case7",
      "matched": true,
      "hard_checks_used": ["主力需同时检查大资金和龙虎榜/知名席位", "不能只用单一资金流字段下结论"]
    }
  ],
  "dimension_scores": {
    "intent_fulfillment": {"raw_score": 0, "evidence": []},
    "data_accuracy_coverage": {"raw_score": 0, "evidence": []},
    "time_caliber_precision": {"raw_score": 0, "evidence": []},
    "analysis_framework_fit": {"raw_score": 0, "evidence": []},
    "insight_extension": {"raw_score": 0, "evidence": []},
    "result_verifiability": {"raw_score": 0, "evidence": []},
    "presentation_visualization": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []},
    "latency_efficiency": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "wrong_analysis_framework",
      "triggered": true,
      "score_ceiling": 55,
      "reason": "答案只用单一资金流字段回答主力问题，遗漏龙虎榜/游资维度。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "reasoning",
      "l2": "market-framework-mismatch",
      "dimension": "analysis_framework_fit",
      "raw_score": 20,
      "confidence": "high",
      "summary": "模型没有把'主力'拆成大资金和游资席位两层市场语义，导致诊断框架错位。",
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

## 字段规则

- `schema_version`：固定为 `stock-diagnosis-data-lookup/v1`。
- `weight_assignment`：包含所有维度（含 `not_applicable`），`not_applicable` 维度的 `dynamic_weight` 为 0。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表。
- `matched_golden_cases`：记录命中的专家案例、图片锚点和 hard checks；未命中时允许为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度。每个维度只输出 `raw_score`（0/20/40/60/80/100 六档整数）和 `evidence`。
- `caps`：包含所有触发的封顶规则；也可包含已检查但未触发的重要封顶规则。
- `root_causes`：有序数组，按重要程度排列。所有活跃维度 raw_score >= 60 且无封顶触发时允许为空，否则至少一个根因。
- `narrative_review`：保持简短可执行。

## 证据对象格式

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output | timing | online_signal",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output | timing.total_seconds | online_dimension_signals[0]",
  "summary": "简短的证据摘要"
}
```

评分时以 `text_answer` 为主锚点。仅在评估可视化、截图、表格和 markdown 呈现时引用 `answer`。

## 序列化规则

- 不输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`；这些由调用方代码自动计算。
- 不输出长引文。
- 证据摘要应短、可定位、可复核。
