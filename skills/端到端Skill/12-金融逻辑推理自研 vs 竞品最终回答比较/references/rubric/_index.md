# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“建议权重”是 result-only 回退权重，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `financial_logic_chain` 金融逻辑链 | 25 | [financial_logic_chain.md](financial_logic_chain.md) | **始终 relevant**。判断最终回答是否把事实、驱动、个股属性和证据推成完整投资逻辑 |
| `market_driver_identification` 市场驱动识别 | 20 | [market_driver_identification.md](market_driver_identification.md) | **relevant**: 涉及热点、催化、题材、资金、技术面、基本面或走势预测。**supplementary**: 静态比较但仍需解释市场为什么定价 |
| `evidence_to_conclusion` 证据到结论 | 25 | [evidence_to_conclusion.md](evidence_to_conclusion.md) | **始终 relevant**。判断最终回答中的证据是否真的支撑结论，而非堆数据 |
| `comparison_and_ranking` 比较与排序 | 15 | [comparison_and_ranking.md](comparison_and_ranking.md) | **relevant**: 用户要求多股选择、谁更强、谁更稳、最受益、排序或优先级。**supplementary**: 单股判断中存在隐含参照。**not_applicable**: 完全无比较或排序需求 |
| `scenario_risk_reasoning` 情景与风险推理 | 10 | [scenario_risk_reasoning.md](scenario_risk_reasoning.md) | **relevant**: 预测、操作建议、追涨、涨停、后市、风险推演。**supplementary**: 一般筛选或比较。**not_applicable**: 只问历史事实且不涉及未来判断 |
| `decision_value_expression` 决策价值表达 | 5 | [decision_value_expression.md](decision_value_expression.md) | **supplementary**: 多数题目均需可用表达。**relevant**: 用户要求操作建议、怎么选、能否追、后市怎么做 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 权重 = 0。
3. 权重总和必须 = 100。
4. 决策任务不同，权重可调整：
   - 预测和操作建议：提高 `scenario_risk_reasoning`、`market_driver_identification` 和 `evidence_to_conclusion`；
   - 多股选择或板块内比较：提高 `comparison_and_ranking` 和 `financial_logic_chain`；
   - 短线强势或涨停题：提高 `market_driver_identification` 和 `evidence_to_conclusion`；
   - 价值/潜力筛选：提高 `financial_logic_chain` 和 `evidence_to_conclusion`。
5. 权重分配须附简短理由（记录在输出的 `weight_assignment[*].rationale` 中）。

## 封顶规则

- [unsupported_prediction_or_recommendation（标签上限 45）](cap_unsupported_prediction_or_recommendation.md)
- [evidence_conclusion_disconnect（标签上限 50）](cap_evidence_conclusion_disconnect.md)
- [missing_key_market_driver（标签上限 55）](cap_missing_key_market_driver.md)
- [overconfident_risk_commitment（标签上限 45）](cap_overconfident_risk_commitment.md)
- [comparison_logic_error（标签上限 60）](cap_comparison_logic_error.md)
- [data_dump_without_reasoning（标签上限 55）](cap_data_dump_without_reasoning.md)

## 封顶规则注意事项

- 封顶规则在本 result-only skill 中作为质量标签记录在 `applied_caps`，不直接改写分数。
- 标签不替代维度评分；同一问题仍需完成所有活跃维度评分。
- 若最终回答出现结论与证据脱节、关键市场驱动缺失、风险承诺过度或比较逻辑错误，应优先检查对应封顶标签。
