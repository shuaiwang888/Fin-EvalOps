# `tool` — 选择与执行工具

当工具选择错误、参数错误或工具约束处理失败时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-tool-selection` | 用错工具，如结构化行情不用 FinQuery，非公开资料不搜索，分时问题不用分时数据 | tool_usage, data_accuracy_coverage |
| `tool-input-error` | 查询条件、时间参数、标的映射、后缀、行业口径或合约输入错误 | tool_usage, time_caliber_precision |
| `tool-limit-not-handled` | 工具上限或失败后未换策略，如 500 根 K 线超过上限后兜底出错 | tool_usage, data_accuracy_coverage |
| `sql-condition-parse-error` | 条件解析错误，如"一个月前上市"、"前 5 日一共涨幅"被 SQL 错解 | tool_usage, time_caliber_precision |
| `missing-cross-check` | 空结果、异常值或关键结论未做二次核验 | tool_usage, result_verifiability |
| `inefficient-tool-strategy` | 反复无效查询、未批量化、无质量收益的低效链路 | tool_usage |
