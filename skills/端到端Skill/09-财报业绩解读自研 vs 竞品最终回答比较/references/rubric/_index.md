# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `intent_understanding` 意图理解与任务完成 | 15 | [intent_understanding.md](intent_understanding.md) | **始终 relevant**。所有题目均考察是否回答用户真正要问的财报问题 |
| `report_data_accuracy` 财报数据与口径准确性 | 18 | [report_data_accuracy.md](report_data_accuracy.md) | **relevant**: 涉及具体财务指标、报告期、同比环比、分红、估值、股价或会计口径。**supplementary**: 纯定性财报讨论 |
| `primary_evidence_quality` 公告全文与证据质量 | 20 | [primary_evidence_quality.md](primary_evidence_quality.md) | **relevant**: 需要公告全文、年报附注、季报说明、会计差错公告、官网公告、业绩说明会、审计意见或行业数据。**supplementary**: 简单指标解释 |
| `causal_attribution_depth` 归因深度 | 18 | [causal_attribution_depth.md](causal_attribution_depth.md) | **relevant**: 用户问为什么、原因、怎么看、发生了什么、差异为什么大。**supplementary**: 单纯查询披露内容 |
| `business_financial_linkage` 业务财务联动 | 12 | [business_financial_linkage.md](business_financial_linkage.md) | **relevant**: 需要把财务变化连接到业务、行业、价格、订单、成本、产品结构、会计政策或特殊事件。**supplementary**: 纯会计口径查询 |
| `forward_investment_judgment` 前瞻与投资判断 | 12 | [forward_investment_judgment.md](forward_investment_judgment.md) | **relevant**: 用户问利好利空、股价影响、能否维持、市场预期、怎么看后续。**not_applicable**: 只问历史披露事实 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary**。表达质量始终有参考价值 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，从 `not_applicable` 或低相关维度让出权重。
3. `supplementary` 维度保留低权重，通常 3-10。
4. `not_applicable` 维度权重 = 0，评分阶段跳过。
5. 所有动态权重之和必须 = 100。
6. 权重分配须附简短理由，记录在输出的 `weight_assignment[*].rationale` 中。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接满足用户真实意图，而非只给背景、数据或泛泛建议。
- 是否给出明确结论、主因、方向、持续性或可执行判断。
- 是否存在报告期、公司、指标、金额、同比环比、口径、会计政策、事实或边界错误。
- 是否覆盖用户要求的关键子问题、对象范围、比较维度和必要解释。
- 结论与理由是否闭合，是否有跳步、偷换概念或因果断裂。
- 关键断言是否有证据支撑，是否可验证。
- 是否把财务结果拆到业务、行业、成本、订单、产品结构、会计处理或特殊事件。
- 涉及股价影响、利好利空、估值或持续性时，是否给出审慎的条件和观察指标。
- 是否尊重“最新/最近/截至某日/报告期/公告后走势”等时间边界。

## 封顶标签

- [hard_fact_or_caliber_error（参考上限 40）](cap_hard_fact_or_caliber_error.md)
- [missing_primary_disclosure（参考上限 55）](cap_missing_primary_disclosure.md)
- [wrong_special_event_explanation（参考上限 45）](cap_wrong_special_event_explanation.md)
- [surface_financial_formula_only（参考上限 60）](cap_surface_financial_formula_only.md)
- [unverifiable_or_hallucinated_numbers（参考上限 50）](cap_unverifiable_or_hallucinated_numbers.md)
- [missing_required_conclusion（参考上限 65）](cap_missing_required_conclusion.md)

## 封顶标签注意事项

- 本类别沿用原规则：封顶规则作为质量标签记录在 `applied_caps`，不直接修改 `final_score`。
- 封顶标签不替代维度评分；触发标签后仍需完成逐维评分。
- 封顶标签只能依据最终回答文本触发。

## 维度边界区分

- `primary_evidence_quality` vs `report_data_accuracy`：前者看最终回答是否呈现了足够权威且贴合问题的证据，后者看数字、报告期、同比环比、会计口径是否正确。
- `causal_attribution_depth` vs `business_financial_linkage`：前者看是否拆出主因、次因、对冲项和特殊事项，后者看是否把这些因素连接到真实业务、行业机制和公司经营变量。
- `forward_investment_judgment` vs `composition_credibility`：前者看投资含义、持续性和观察指标是否可验证，后者看最终回答是否结构清楚、措辞审慎、重点突出。
