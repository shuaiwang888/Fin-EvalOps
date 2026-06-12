# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短的自然语言评审。

## JSON 结构

```json
{
  "schema_version": "kyc-recommendation-suggestions/v1",
  "weight_assignment": {
    "intent_profile_understanding": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "用户要求结合自身情况推荐"},
    "scenario_emotion_recognition": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户表达持续亏损和迷茫，需要识别真实处境"},
    "suitability_personalization": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "推荐必须匹配用户风险、期限和资金目标"},
    "evidence_integration": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需要市场和标的证据支撑推荐"},
    "decision_actionability": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "用户需要可执行的买卖和仓位建议"},
    "risk_boundary_control": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "推荐建议必须有风险边界和证伪条件"},
    "composition_credibility": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达清晰度影响用户理解"},
    "tool_usage": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "链路需要核验是否主动使用 KYC 数据和合适工具支撑推荐"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "case13_loss_confusion",
      "matched_reason": "用户表达迷茫和亏损感",
      "hard_checks_used": ["不得直接切到短线荐股", "应先识别情绪和风险状态"]
    }
  ],
  "dimension_scores": {
    "intent_profile_understanding": {"raw_score": 0, "evidence": []},
    "scenario_emotion_recognition": {"raw_score": 0, "evidence": []},
    "suitability_personalization": {"raw_score": 0, "evidence": []},
    "evidence_integration": {"raw_score": 0, "evidence": []},
    "decision_actionability": {"raw_score": 0, "evidence": []},
    "risk_boundary_control": {"raw_score": 0, "evidence": []},
    "composition_credibility": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "missing_kyc_profile",
      "triggered": true,
      "score_ceiling": 60,
      "reason": "05 类推荐建议问题理当使用用户 KYC 数据，但链路和最终答案都未体现 KYC 使用，回答变成通用推荐。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "context",
      "l2": "missing-kyc-usage",
      "dimension": "suitability_personalization",
      "raw_score": 1,
      "confidence": "high",
      "summary": "本题属于 KYC 推荐建议场景，模型应使用用户 KYC 数据但未使用，导致推荐依据无法证明适合该用户。",
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

> **注意**：`weighted_points`、`absolute_score_pre_cap`、`final_score` 由调用方代码自动计算，你不需要输出这些字段。你只需输出每个维度的 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`。

## 证据对象格式

使用紧凑的证据条目：

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

指针格式对应输入数据结构：

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案的纯文本版本 |
| `context` | `context[N].question` / `context[N].answer` | 对话中第 N 轮历史问题或答案 |
| `reasoning` | `chain[N].plan` | 第 N 步的规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用（含 name + input） |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具调用的输出 |

评分时以 `text_answer` 为主锚点。KYC 画像相关评分必须检查最终答案是否体现用户 KYC 数据，也必须检查链路中是否主动读取、调用、检索或引用用户 KYC 数据。`context` 只是可能的数据来源之一；不要因 `context` 没有 KYC 就放过“应使用 KYC 但未使用”的问题。不要因隐藏链路中出现好判断而给最终答案加分。

除非调用方明确要求，不要输出长引文。

## 字段规则

- `schema_version`：固定为 `kyc-recommendation-suggestions/v1`。
- `weight_assignment`：每个维度的动态权重分配结果。包含 `dynamic_weight`、`applicability`、`rationale`。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表。这些维度不出现在 `dimension_scores` 中。
- `matched_golden_cases`：记录命中的专家案例和实际使用的 hard checks；未命中时允许为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，不含 `skipped_dimensions` 中的维度。每个维度只需输出 `raw_score` 和 `evidence`。
- `caps`：包含所有考虑过的封顶规则（仅与活跃维度相关的），或至少包含所有触发的封顶规则。
- `root_causes`：有序数组，按重要程度排列。仅在合格通过（所有活跃维度 raw_score >= 60 且无封顶触发）时允许返回空数组。否则必须返回至少一个根因。
- `root_causes[*].dimension`：该根因所解释的维度。
- `root_causes[*].raw_score`：该维度的 raw_score，用于可追溯性。
- 若主要问题是没有使用 KYC，`root_causes[*].summary` 必须明确包含“应使用用户 KYC 数据但未使用”或同义说明，便于归因聚合。
- `narrative_review`：保持简短且可执行。

## 叙事评审模板

保持可读且简洁：
- `summary`：一段话概括整体判断
- `strengths`：仅列出真正的优势
- `weaknesses`：驱动分数的主要不足
- `next_actions`：产品和算法团队可以执行的修复建议

## 序列化规则

在机器可读性和文字表现力之间选择时，优先保持 JSON 稳定，缩短叙事。
