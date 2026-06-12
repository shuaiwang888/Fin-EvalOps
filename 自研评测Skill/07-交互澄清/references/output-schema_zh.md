# 输出格式规范

先输出结构化 JSON。需要可读摘要时，在 JSON 后附简短自然语言评审。

```json
{
  "schema_version": "interactive-clarification/v1",
  "weight_assignment": {
    "intent_fulfillment": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "用户询问是否能回本，核心是澄清目标识别"},
    "ambiguity_clarification": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "缺少持仓成本、亏损幅度和时间目标"},
    "context_continuity": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "用户第二轮补充持仓信息，需承接前轮澄清框架"},
    "entity_resolution": {"dynamic_weight": 0, "applicability": "not_applicable", "rationale": "标的名称清楚，无错别字或异常代码"},
    "financial_rule_and_premise": {"dynamic_weight": 8, "applicability": "supplementary", "rationale": "需避免给出违反交易规则的操作建议"},
    "assumption_definition": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "回本方案需要定义持仓周期、风险承受和目标收益"},
    "actionability_and_risk_plan": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "用户补充信息后需把回本路径落到可执行方案"},
    "evidence_grounding": {"dynamic_weight": 8, "applicability": "relevant", "rationale": "需用行情和基本面信息支撑建议"},
    "guidance_and_retention": {"dynamic_weight": 6, "applicability": "supplementary", "rationale": "可通过后续监控和复查形成澄清闭环"},
    "tool_usage": {"dynamic_weight": 6, "applicability": "relevant", "rationale": "需检查标的行情、工具调用和规则核验"},
    "latency_efficiency": {"dynamic_weight": 2, "applicability": "supplementary", "rationale": "交互澄清场景耗时影响体验但非核心正确性"}
  },
  "skipped_dimensions": ["entity_resolution"],
  "matched_golden_cases": [
    {
      "case_id": "case01_recover_loss_after_buying_this_month",
      "matched_reason": "用户表达回本诉求且缺少持仓/亏损变量",
      "hard_checks_used": ["先确认持仓、成本、亏损幅度和时间目标", "用户补充后必须沿首轮回本框架推进"]
    }
  ],
  "dimension_scores": {
    "intent_fulfillment": {"raw_score": 0, "evidence": []},
    "ambiguity_clarification": {"raw_score": 0, "evidence": []},
    "context_continuity": {"raw_score": 0, "evidence": []},
    "financial_rule_and_premise": {"raw_score": 0, "evidence": []},
    "assumption_definition": {"raw_score": 0, "evidence": []},
    "actionability_and_risk_plan": {"raw_score": 0, "evidence": []},
    "evidence_grounding": {"raw_score": 0, "evidence": []},
    "guidance_and_retention": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []},
    "latency_efficiency": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "context_break_after_clarification",
      "triggered": false,
      "score_ceiling": 55,
      "reason": "",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "context",
      "l2": "clarification_not_followed",
      "dimension": "context_continuity",
      "raw_score": 20,
      "confidence": "high",
      "summary": "首轮要求用户补充亏损和持仓信息，但二轮没有使用这些变量制定回本路径。",
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

- `schema_version`：固定为 `interactive-clarification/v1`。
- `weight_assignment`：包含全部维度。所有 `dynamic_weight` 之和必须等于 100。
- `applicability`：只能取 `relevant`、`supplementary`、`not_applicable`。
- `skipped_dimensions`：列出所有 `not_applicable` 维度；这些维度不出现在 `dimension_scores`。
- `matched_golden_cases`：记录命中的专家案例、图片批注锚点和实际使用的 hard checks；未命中时允许为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度。每个维度只输出 `raw_score` 和 `evidence`。
- `raw_score`：只取 0、20、40、60、80、100 六档整数。
- `caps`：至少包含所有触发的封顶规则；也可包含已检查但未触发的重要封顶规则。
- `root_causes`：有序数组，按重要程度排列。所有活跃维度 raw_score >= 60 且无封顶触发时允许为空，否则至少一个根因。
- 不输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`；这些由调用方代码计算。

## 证据对象

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output | timing | online_signal | human_review",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output | timing.total_seconds | online_dimension_signals[0] | human_review_feedback[0]",
  "summary": "简短证据摘要"
}
```

评分时以 `text_answer` 为主锚点。仅在评估截图、表格、markdown 呈现、图片批注或答案后引导时引用 `answer`。

## 序列化规则

- JSON 必须可解析，不要输出注释。
- 证据摘要应短、可定位、可复核。
- 叙事评审只写主要判断、主要不足和可执行修复建议。
