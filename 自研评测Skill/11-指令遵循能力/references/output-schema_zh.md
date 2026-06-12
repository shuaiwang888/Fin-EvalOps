# 输出格式规范

先输出结构化 JSON；如需可读摘要，在 JSON 后附简短自然语言评审。

```json
{
  "schema_version": "instruction-following-ability/v3",
  "instruction_parse": {
    "primary_instruction": "分析领涨原因",
    "constraints": ["截止今天上午9点36分", "赛马概念", "海南橡胶也涨"],
    "expected_answer_type": "cause_analysis"
  },
  "weight_assignment": {
    "explicit_instruction_completion": {"dynamic_weight": 30, "applicability": "relevant", "rationale": "用户明确要求原因"},
    "task_type_alignment": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "原因分析不能替换成行情播报"},
    "constraint_coverage": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需覆盖时点、概念和个股"},
    "answer_focus": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需围绕原因而非数据堆砌"},
    "necessary_information_completeness": {"dynamic_weight": 10, "applicability": "supplementary", "rationale": "原因需有必要证据"},
    "tool_usage": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需评估工具是否服务主指令"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "dimension_scores": {
    "explicit_instruction_completion": {"raw_score": 60, "evidence": []},
    "task_type_alignment": {"raw_score": 60, "evidence": []},
    "constraint_coverage": {"raw_score": 60, "evidence": []},
    "answer_focus": {"raw_score": 60, "evidence": []},
    "necessary_information_completeness": {"raw_score": 60, "evidence": []},
    "tool_usage": {"raw_score": 60, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "primary_instruction_missing",
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
