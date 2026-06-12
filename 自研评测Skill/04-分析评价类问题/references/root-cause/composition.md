# `composition` — 组织答案

当链路中可能有正确理解或信息，但最终答案组织不佳、表达不可信或关键逻辑没有呈现时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `data-dumping` | 长表格、指标或资讯替代投资论点，缺少解释 | composition_credibility, investment_logic_depth |
| `generic-template-answer` | 对不同标的套同一模板，不能体现个股差异 | composition_credibility, method_fit |
| `vague-subjective-style` | 表述含糊、过度主观、没有可验证依据，如“市场关注”“逻辑较好”但无说明 | composition_credibility |
| `plan-answer-drop` | 链路里有关键判断或工具结果，最终答案没有呈现 | composition_credibility, evidence_source_quality |
| `no-clear-conclusion` | 用户需要判断或行动建议，但答案没有清晰结论、条件或风险 | actionability_risk |
| `fact-opinion-boundary-blurred` | 没有区分事实、推断、观点和不确定性 | composition_credibility |
| `generic-personal-advice` | 个人化推荐看似完整，但像通用投顾模板，缺少“为什么适合我”“为什么现在这样配”和行动边界 | composition_credibility, user_profile_suitability |

证据优先看 `chain.plan` 与 `text_answer` 的差异。
