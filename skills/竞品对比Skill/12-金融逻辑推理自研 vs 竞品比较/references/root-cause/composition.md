# `composition` — 答案组织

当系统可能有部分逻辑但最终答案没有清楚呈现成用户可用判断时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `data-dump-no-synthesis` | 股票列表、指标表、公告或行情数据堆砌，缺少综合判断 | decision_value_expression, evidence_to_conclusion |
| `conclusion-not-actionable` | 答案没有形成清晰选择、排序、操作建议或观察条件 | decision_value_expression |
| `risk-boundary-not-presented` | 风险和失效条件没有被明确呈现 | scenario_risk_reasoning, decision_value_expression |
| `ranking-presentation-unclear` | 比较和排序有材料但主次、标准或结论不清 | comparison_and_ranking |
| `generic-template` | 使用泛泛模板化表达，没有针对具体标的和场景组织答案 | financial_logic_chain, decision_value_expression |
| `key-judgment-buried` | 核心判断被埋在长背景、长表格或分散段落中 | decision_value_expression |

如果最终答案表达清楚但逻辑本身错误，应优先归因到 `reasoning`。
