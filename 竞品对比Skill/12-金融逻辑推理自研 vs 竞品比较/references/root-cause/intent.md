# `intent` — 理解决策任务

当系统没有正确理解用户要做的金融决策任务时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `decision-task-misread` | 把预测、筛选、比较、排序、操作建议或风险推演任务理解错 | financial_logic_chain, decision_value_expression |
| `decision-object-misread` | 股票、板块、概念、行业或股票池对象识别错误 | financial_logic_chain, comparison_and_ranking |
| `time-horizon-missed` | 忽略明天、下周、近期、截至某日等时间期限 | market_driver_identification, scenario_risk_reasoning |
| `comparison-intent-missed` | 用户要求怎么选、谁更强、谁更稳或排序，但答案未识别比较意图 | comparison_and_ranking |
| `risk-intent-missed` | 用户问能否追、后市怎么操作或风险情景，但答案没有识别风险和条件需求 | scenario_risk_reasoning, decision_value_expression |

归因时要先看用户问题本身，再看最终答案是否围绕该任务展开。
