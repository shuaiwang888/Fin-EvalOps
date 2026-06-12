# `intent` — 理解问题

当系统误解或低估用户真实诊股查数需求时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `surface-query-only` | 只按表层关键词取数，未识别诊断、对比、解释或决策语义 | intent_fulfillment, analysis_framework_fit |
| `subtask-missed` | 遗漏子任务，如只列数据不算差值，只查资金不查龙虎榜，只给价格不讲止盈逻辑 | intent_fulfillment, calculation_comparison |
| `scope-constraint-missed` | 忽略标的、时间、市场、行业、条件、非 ST/非科创等约束 | intent_fulfillment, data_accuracy_coverage |
| `ambiguous-time-not-resolved` | 对模糊时间未做合理锚定，如"什么时候分红"未同时回答最近事件和今年进展 | time_caliber_precision, intent_fulfillment |
