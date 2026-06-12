# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "time-awareness-ability-self-vs-competitor/v1",
  "pairing": {
    "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "time_anchor_analysis": {
    "request_time": "2026-04-07 Asia/Shanghai",
    "extracted_time_expressions": ["今天"],
    "resolved_time_targets": [
      {
        "expression": "今天",
        "resolved_date": "2026-04-07",
        "market_or_entity": "港股 / 小米集团-W(01810.HK)",
        "expected_boundary": "港股当日休市，无当日交易；若使用行情，应标注上一交易日 as-of"
      }
    ],
    "confidence": "high"
  },
  "weight_assignment": {
    "temporal_intent_recognition": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户用今天询问个股涨跌，必须识别时间前提。"},
    "anchor_date_resolution": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "需要把今天锚定到请求日期。"},
    "market_calendar_status": {"dynamic_weight": 25, "applicability": "relevant", "rationale": "目标为港股，是否交易是主前提。"},
    "data_asof_freshness": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "需避免旧行情冒充今日行情。"},
    "period_disclosure_mapping": {"dynamic_weight": 0, "applicability": "not_applicable", "rationale": "问题不涉及财报或分红报告期。"},
    "premise_correction_clarification": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "若当天无交易，必须纠正用户前提。"},
    "answer_composition_credibility": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达清楚度影响用户是否理解时间边界。"},
    "tool_usage": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需要检查链路是否核验交易日历和行情日期。"}
  },
  "skipped_dimensions": ["period_disclosure_mapping"],
  "matched_golden_cases": [
    {
      "case_id": "Case 2",
      "case_name": "港股休市日问小米今天为什么跌了",
      "used_hard_checks": [
        "当天休市时必须先说明无交易。",
        "引用上一交易日行情必须标注具体日期和 as-of。"
      ]
    }
  ],
  "self_evaluation": {
    "dimension_scores": {
      "temporal_intent_recognition": {"raw_score": 0, "evidence": []},
      "anchor_date_resolution": {"raw_score": 0, "evidence": []},
      "market_calendar_status": {"raw_score": 0, "evidence": []},
      "data_asof_freshness": {"raw_score": 0, "evidence": []},
      "premise_correction_clarification": {"raw_score": 0, "evidence": []},
      "answer_composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [
      {
        "rule_id": "market_closed_answered_as_open",
        "triggered": false,
        "score_ceiling": 35,
        "reason": "",
        "evidence": []
      }
    ],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "temporal_intent_recognition": {"raw_score": 0, "evidence": []},
      "anchor_date_resolution": {"raw_score": 0, "evidence": []},
      "market_calendar_status": {"raw_score": 0, "evidence": []},
      "data_asof_freshness": {"raw_score": 0, "evidence": []},
      "premise_correction_clarification": {"raw_score": 0, "evidence": []},
      "answer_composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [
      {
        "rule_id": "market_closed_answered_as_open",
        "triggered": false,
        "score_ceiling": 35,
        "reason": "",
        "evidence": []
      }
    ],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "dimension_comparison": {
    "temporal_intent_recognition": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "anchor_date_resolution": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "market_calendar_status": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "data_asof_freshness": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "premise_correction_clarification": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "answer_composition_credibility": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    },
    "tool_usage": {
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
  "chain_attribution": {
    "self": [
      {"stage": "intent | evidence | tool | reasoning | composition | capability_gap", "summary": "", "evidence": []}
    ],
    "competitor": [
      {"stage": "intent | evidence | tool | reasoning | composition | capability_gap", "summary": "", "evidence": []}
    ],
    "cross_model_observations": []
  },
  "comparison_summary": {
    "absolute_summary": "",
    "relative_summary": "",
    "verdict": "self_better | competitor_better | tie | both_poor",
    "why": []
  }
}
```

## 字段规则

- `schema_version`：固定为 `time-awareness-ability-self-vs-competitor/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识，用于回溯原始样本。
- `pairing.self_model_id`：固定为 `"self"`（被评测的自研模型）。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `time_anchor_analysis`：同一题下双方共享的时间锚点解析，只能依据用户问题、必要上下文和请求时间生成，不得因某一方答案改变。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：标记为 `not_applicable` 的维度列表。这些维度不出现在两边的 `dimension_scores` 和 `dimension_comparison` 中。
- `matched_golden_cases`：命中的专家案例和实际使用的 hard checks。未命中可为空数组。
- `self_evaluation` / `competitor_evaluation`：分别是两边的绝对评测结果，结构遵循本 skill 定义的维度、封顶和根因体系。
- `dimension_scores`：仅包含活跃维度。每个维度只输出 `raw_score`（严格取 0/20/40/60/80/100 之一）和 `evidence`；不要输出 `weighted_points`、`absolute_score_pre_cap` 或 `final_score`。
- `caps`：包含所有触发的封顶规则，或所有与活跃维度相关且被显式检查过的封顶规则。每条含 `rule_id`、`triggered`、`score_ceiling`、`reason`、`evidence`。
- `root_causes`：有序数组，按重要程度排列。若所有活跃维度 `raw_score >= 60` 且无封顶触发，可为空数组；否则至少一个。
- `root_causes[*].l1`：必须来自 `intent/evidence/tool/reasoning/composition/capability_gap`。
- `root_causes[*].confidence`：`high/medium/low`。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据。`score_delta = self_raw_score - competitor_raw_score`。示例中跳过了 `period_disclosure_mapping`；若该维度为活跃维度，必须同步加入两边 `dimension_scores` 和 `dimension_comparison`。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品真正值得学习的地方，必须有答案或链路证据。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `chain_attribution`：解释链路如何导致最终答案更好/更差；不要脱离答案单独评价链路“是否漂亮”。
- `comparison_summary.absolute_summary`：先写双方按专家标准各自好不好。
- `comparison_summary.relative_summary`：再写双方谁相对更好。
- `comparison_summary.verdict`：若双方都明显不达标，即便一方分数略高，也应使用 `both_poor`。

## 最终答案锚点

- 自研模型最终答案：优先 `self_record.text_answer`；
- 竞品模型最终答案：若 `competitor_record.text_answer` 为空，则使用 `competitor_record.answer`；
- 若编排层已生成统一字段，可读取归一化字段，但证据仍需回指原始字段。

## 证据对象格式

```json
{
  "source": "question | self_final_answer | competitor_final_answer | self_context | competitor_context | self_reasoning | competitor_reasoning | self_function_call | competitor_function_call | self_function_call_output | competitor_function_call_output",
  "pointer": "question | self_record.text_answer | competitor_record.answer | self_record.chain[0].plan | competitor_record.chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

## 证据使用原则

- 评分主锚点仍是双方各自最终答案。
- 工具调用证据统一从 `self_record.chain[N].tools[M]` / `competitor_record.chain[N].tools[M]` 读取。
- `tool_usage`、根因归因和比较解释允许引用各自链路。
- 当竞品 `plan` 为空时，不要臆造不可见推理；可直接引用工具调用、工具输出和最终答案。
- 证据摘要应短而具体，优先写清日期、市场、报告期、as-of 或工具返回时间。
- 若一条差异无法追溯到答案或链路证据，不要写成确定结论。

## 叙事评审模板

- `absolute_summary`：先说明双方按时间感知专家标准各自是否合格。
- `relative_summary`：再说明自研相对竞品领先/落后在哪里。
- `why`：仅列真正驱动结论的高信号原因。
