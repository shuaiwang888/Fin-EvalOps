# `tool` — 选择与执行工具

当工具选择错误或使用方式有误时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-tool-selection` | 工具选择错误：用 Search 查 FinQuery 能直接处理的结构化数据；未用 BackTest 进行策略回测；用通用 Search 代替 StockNews/NoticeSearch | tool_usage, data_retrieval_accuracy |
| `tool-input-error` | 工具输入错误：参数格式不对、时间范围参数错误、缺少必要后缀、查询条件表达不准确 | tool_usage, data_retrieval_accuracy |
| `tool-step-error` | 工具执行步骤错误：多步查询未按正确顺序执行、中间结果未正确传递到后续工具调用、AnalysisLib 与其他工具混用 | tool_usage, logical_decomposition |
| `inefficient-tool-strategy` | 工具策略低效：全量统计或复杂回测中反复低效查询、无效重试或没有批量化/结构化取数，导致耗时显著过长且无质量收益 | latency_efficiency, tool_usage |
