# 输出格式规范

先输出结构化 JSON；如需可读摘要，在 JSON 后附简短自然语言评审。

```json
{
  "schema_version": "financial-logical-reasoning/v3",
  "decision_task": {
    "task_type": "stock_selection | trend_forecast | operation_advice | comparison | risk_scenario",
    "decision_object": "用户指定股票、板块或股票池",
    "time_horizon": "明天 | 下周 | 近期 | 未指定"
  },
  "weight_assignment": {
    "financial_logic_chain": {"dynamic_weight": 25, "applicability": "relevant", "rationale": "需要完整投资逻辑"},
    "market_driver_identification": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "需识别热点、催化或价格驱动"},
    "evidence_to_conclusion": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "证据需支撑结论"},
    "comparison_and_ranking": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "用户要求多股选择"},
    "scenario_risk_reasoning": {"dynamic_weight": 10, "applicability": "supplementary", "rationale": "投资建议需给风险情景"},
    "decision_value_expression": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "需有可执行表达"},
    "tool_usage": {"dynamic_weight": 5, "applicability": "relevant", "rationale": "需评估工具是否支撑推理"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "dimension_scores": {
    "financial_logic_chain": {"raw_score": 0, "evidence": []},
    "market_driver_identification": {"raw_score": 0, "evidence": []},
    "evidence_to_conclusion": {"raw_score": 0, "evidence": []},
    "comparison_and_ranking": {"raw_score": 0, "evidence": []},
    "scenario_risk_reasoning": {"raw_score": 0, "evidence": []},
    "decision_value_expression": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "unsupported_prediction_or_recommendation",
      "triggered": false,
      "score_ceiling": 45,
      "reason": "",
      "evidence": []
    }
  ],
  "root_causes": [],
  "narrative_review": {
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "next_actions": []
  }
}
```

证据对象：
```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短证据摘要"
}
```

不要输出加权分、总分或最终分；调用方代码负责计算。
