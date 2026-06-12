# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `intent_understanding` 意图理解与任务完成 | 15 | [intent_understanding.md](intent_understanding.md) | **始终 relevant**。所有题目均考察是否回答用户真正要问的财报问题 |
| `report_data_accuracy` 财报数据与口径准确性 | 15 | [report_data_accuracy.md](report_data_accuracy.md) | **relevant**: 涉及具体财务指标、报告期、同比环比、分红、估值、股价或会计口径。**supplementary**: 纯定性财报讨论 |
| `primary_evidence_quality` 公告全文与证据质量 | 15 | [primary_evidence_quality.md](primary_evidence_quality.md) | **relevant**: 需要公告全文、年报附注、季报说明、会计差错公告、官网公告、业绩说明会或行业数据。**supplementary**: 简单指标解释 |
| `causal_attribution_depth` 归因深度 | 15 | [causal_attribution_depth.md](causal_attribution_depth.md) | **relevant**: 用户问为什么、原因、怎么看、发生了什么、差异为什么大。**supplementary**: 单纯查询披露内容 |
| `business_financial_linkage` 业务财务联动 | 10 | [business_financial_linkage.md](business_financial_linkage.md) | **relevant**: 需要把财务变化连接到业务、行业、价格、订单、成本、产品结构、会计政策或特殊事件。**supplementary**: 纯会计口径查询 |
| `forward_investment_judgment` 前瞻与投资判断 | 10 | [forward_investment_judgment.md](forward_investment_judgment.md) | **relevant**: 用户问利好利空、股价影响、能否维持、市场预期、怎么看后续。**not_applicable**: 只问历史披露事实 |
| `composition_credibility` 表达可信度 | 5 | [composition_credibility.md](composition_credibility.md) | **始终 supplementary**。表达质量始终有参考价值 |
| `tool_usage` 工具使用合理性 | 15 | [tool_usage.md](tool_usage.md) | **始终 relevant**。财报题必须评估结构化数据、公告全文、搜索和交叉验证策略 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重（建议 3-5）
3. `not_applicable` 维度权重 = 0，评分阶段跳过
4. 所有动态权重之和必须 = 100
5. 权重分配须附简短理由（记录在输出的 `weight_assignment[*].rationale` 中）

## 封顶规则

- [hard_fact_or_caliber_error（上限 40）](cap_hard_fact_or_caliber_error.md)
- [missing_primary_disclosure（上限 55）](cap_missing_primary_disclosure.md)
- [wrong_special_event_explanation（上限 45）](cap_wrong_special_event_explanation.md)
- [surface_financial_formula_only（上限 60）](cap_surface_financial_formula_only.md)
- [unverifiable_or_hallucinated_numbers（上限 50）](cap_unverifiable_or_hallucinated_numbers.md)
- [missing_required_conclusion（上限 65）](cap_missing_required_conclusion.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 更好的隐藏规划不会覆盖最终答案触发的封顶规则。
- 如果答案推理看似自洽但遗漏公司明确披露的核心事件，应优先考虑 `missing_primary_disclosure` 或 `wrong_special_event_explanation`。
