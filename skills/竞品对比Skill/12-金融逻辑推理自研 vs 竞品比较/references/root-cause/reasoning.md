# `reasoning` — 投资逻辑推导

当系统没有把证据推导成有决策价值的金融结论时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `broken-investment-logic-chain` | 金融事实、市场驱动、个股属性和结论之间链条断裂 | financial_logic_chain |
| `market-driver-missed` | 未识别真正影响未来表现的热点、催化、资金、技术或基本面驱动 | market_driver_identification |
| `evidence-conclusion-disconnect` | 证据不能支撑结论，或数据与推荐之间缺少传导解释 | evidence_to_conclusion |
| `comparison-standard-missing` | 多股比较或排序缺少统一标准 | comparison_and_ranking |
| `scenario-risk-missing` | 预测或操作建议没有情景、条件和风险边界 | scenario_risk_reasoning |
| `overconfident-inference` | 把概率性判断写成确定性收益或确定涨停 | scenario_risk_reasoning, decision_value_expression |
| `single-factor-reasoning` | 用单一指标替代完整投资逻辑 | financial_logic_chain, evidence_to_conclusion |
| `static-data-over-dynamic-market` | 用静态数据覆盖短线热点、题材发酵和资金驱动 | market_driver_identification |

若工具已经收集到足够证据，但答案没有推导出结论，本 L1 通常优先于 `evidence`。
