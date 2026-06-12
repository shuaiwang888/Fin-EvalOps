# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

输出形态与既有 self_judge schema 保持一致：动态权重、跳过维度、专家案例、维度原始分、封顶、根因、叙事评审。调用方负责计算加权分和最终分。

## JSON 结构

```json
{
  "schema_version": "time-awareness-ability/v1",
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
      "triggered": true,
      "score_ceiling": 35,
      "reason": "目标市场当天休市，但答案按当日交易解释涨跌。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "reasoning",
      "l2": "premise-not-rejected",
      "dimension": "premise_correction_clarification",
      "raw_score": 1,
      "confidence": "high",
      "summary": "答案没有否定休市日仍发生当日交易的错误前提，导致旧行情被解释成今天涨跌。",
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
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短证据摘要"
}
```

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案纯文本 |
| `context` | `context[N].answer` | 第 N 轮历史答案 |
| `reasoning` | `chain[N].plan` | 第 N 步规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用 |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具输出 |

不要输出长引文；证据摘要应短而具体，优先写清日期、市场、报告期、as-of 或工具返回时间。

## 字段规则

- `schema_version`：固定为 `time-awareness-ability/v1`。
- `time_anchor_analysis`：记录本题时间锚点解析；请求时间缺失时 `request_time` 写 `unknown`，`confidence` 降低。
- `weight_assignment`：包含全部维度。每个维度有 `dynamic_weight`、`applicability`、`rationale`。所有动态权重之和必须等于 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表；这些维度不出现在 `dimension_scores` 中。
- `matched_golden_cases`：命中的专家案例和实际使用的 hard checks。未命中可为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度。每个维度只输出 `raw_score` 和 `evidence`。
- `caps`：包含所有触发的封顶规则；若无触发可为空数组。也可包含已检查但未触发的重要规则。
- `root_causes`：按重要程度排列。若所有活跃维度 raw_score >= 60 且无封顶触发，可为空数组；否则至少一个。
- `root_causes[*].l1`：必须来自 `intent/evidence/tool/reasoning/composition/capability_gap`。
- `root_causes[*].confidence`：`high/medium/low`。
- `narrative_review`：保持简短，重点写可执行改进建议。

## 序列化规则

- 不要输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`，这些由调用方代码计算。
- JSON 优先，叙事简短。
- 若评分依据不足，必须在 `time_anchor_analysis`、`evidence` 或 `root_causes` 中体现低置信，而不是编造证据。
