# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `financial_logic_chain` 金融逻辑链完整性 | 25 | [financial_logic_chain.md](financial_logic_chain.md) | **始终 relevant**。是否形成从事实到结论的闭环 |
| `market_driver_identification` 市场驱动识别 | 20 | [market_driver_identification.md](market_driver_identification.md) | 短线、热点、走势、板块题 relevant；纯基本面题 supplementary |
| `evidence_to_conclusion` 证据到结论连接 | 20 | [evidence_to_conclusion.md](evidence_to_conclusion.md) | **始终 relevant**。数据、新闻、公告、资金是否支撑结论 |
| `comparison_and_ranking` 个股比较与排序 | 15 | [comparison_and_ranking.md](comparison_and_ranking.md) | 多股选择、怎么选、推荐、排序时 relevant；单股题 supplementary |
| `scenario_risk_reasoning` 情景与风险推演 | 10 | [scenario_risk_reasoning.md](scenario_risk_reasoning.md) | 预测、追高、操作建议、下周/明天题 relevant |
| `decision_value_expression` 决策价值表达 | 5 | [decision_value_expression.md](decision_value_expression.md) | **始终 supplementary**；操作建议题 relevant |
| `tool_usage` 工具使用合理性 | 5 | [tool_usage.md](tool_usage.md) | **始终 relevant** |

## 动态权重分配规则

1. 预测/操作建议题提高 `scenario_risk_reasoning` 和 `decision_value_expression`。
2. 多股比较题提高 `comparison_and_ranking`。
3. 热点短线题提高 `market_driver_identification`。
4. 纯基本面价值题提高 `financial_logic_chain` 和 `evidence_to_conclusion`。
5. 权重总和必须为 100。

## 封顶规则

- [unsupported_prediction_or_recommendation（上限 45）](cap_unsupported_prediction_or_recommendation.md)
- [wrong_core_investment_logic（上限 50）](cap_wrong_core_investment_logic.md)
- [market_driver_missing（上限 55）](cap_market_driver_missing.md)
- [data_dump_without_reasoning（上限 55）](cap_data_dump_without_reasoning.md)
- [comparison_without_standard（上限 60）](cap_comparison_without_standard.md)
- [risk_scenario_missing_for_high_risk_advice（上限 65）](cap_risk_scenario_missing_for_high_risk_advice.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 若多条同时触发，取最低上限。

## 常见失败

- 便宜有潜力只看估值，甚至选 PE 为负。
- 明天涨停只看连板，不找市场热点和题材情绪。
- 个股走势只解读单个常规公告，忽略前期上涨原因、资金流和机构行为。
- 后市分析用"四大面"模板堆指标，缺少重点。
- 多股怎么选只看技术面，不比较业务占比、弹性、自给率和风险。
