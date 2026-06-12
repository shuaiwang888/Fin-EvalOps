# Rubric 索引

## 动态权重默认值

| 维度 | 默认权重 | 说明 |
|---|---:|---|
| `intent_fulfillment` | 13 | 用户真实澄清目标是否满足。 |
| `ambiguity_clarification` | 17 | 是否识别不能直接答的状态，并问到关键变量。 |
| `context_continuity` | 15 | 用户补充后是否承接前轮澄清框架。 |
| `entity_resolution` | 13 | 错别字、同音、异常代码、简称是否识别正确。 |
| `financial_rule_and_premise` | 15 | 交易规则、权限、税费、计息、错误前提是否纠正。 |
| `assumption_definition` | 8 | 模糊条件是否转成可核验口径。 |
| `actionability_and_risk_plan` | 8 | 澄清或纠错后是否有可执行落地和风险边界。 |
| `evidence_grounding` | 6 | 数据、规则、行情、公告或可见来源是否支撑结论。 |
| `guidance_and_retention` | 5 | 是否形成后续监控、提醒、复查或继续追问闭环。 |

动态权重必须按题目重分配，总和等于 100。例：
- 错别字标的识别题：提高 `entity_resolution` 和 `evidence_grounding`。
- 交易规则陷阱题：提高 `financial_rule_and_premise`。
- 二轮补充持仓题：提高 `context_continuity`。
- 模糊条件选股题：提高 `ambiguity_clarification`、`assumption_definition` 和 `actionability_and_risk_plan`。
- 纯首轮咨询题：`context_continuity` 可为 `not_applicable`。

## Doc 主线校准

07 文档的核心不是泛化投顾能力，而是交互澄清闭环。评分时优先看三条主线：
- **澄清与承接**：首轮能否问到关键变量，用户补充后二轮是否沿前轮框架推进。
- **语义与实体纠错**：是否贴近股民输入习惯处理错别字、同音、异常代码和多义标的。
- **规则与前提纠错**：是否先识别做空、北交所权限、撤单、T+1、分红税、逆回购计息等错误前提。

`actionability_and_risk_plan` 和 `guidance_and_retention` 是澄清闭环的落地延伸，不应压过上述三条主线。

## 维度文件

评分前先读 [raw-score-scale.md](raw-score-scale.md)，再按需读取：
- [intent_fulfillment.md](intent_fulfillment.md)
- [ambiguity_clarification.md](ambiguity_clarification.md)
- [context_continuity.md](context_continuity.md)
- [entity_resolution.md](entity_resolution.md)
- [financial_rule_and_premise.md](financial_rule_and_premise.md)
- [assumption_definition.md](assumption_definition.md)
- [actionability_and_risk_plan.md](actionability_and_risk_plan.md)
- [evidence_grounding.md](evidence_grounding.md)
- [guidance_and_retention.md](guidance_and_retention.md)

## 封顶规则

按需读取：
- [cap_wrong_financial_rule_or_unhandled_invalid_premise.md](cap_wrong_financial_rule_or_unhandled_invalid_premise.md)
- [cap_wrong_entity_resolution.md](cap_wrong_entity_resolution.md)
- [cap_fabricated_or_unsupported_specific_advice.md](cap_fabricated_or_unsupported_specific_advice.md)
- [cap_context_break_after_clarification.md](cap_context_break_after_clarification.md)
- [cap_missing_required_clarification.md](cap_missing_required_clarification.md)
- [cap_inconsistent_time_or_definition_scope.md](cap_inconsistent_time_or_definition_scope.md)
- [cap_generic_template_without_clarification_value.md](cap_generic_template_without_clarification_value.md)

封顶规则在本 result-only 比较 skill 中作为质量标签记录，不替代各维度评分。
