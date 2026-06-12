# L1: tool — 选择与执行工具

是否使用正确工具核验时间信息。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| calendar-tool-missing | 应查交易日历、行情日历或市场状态但未调用 | tool_usage |
| wrong-tool-date-input | 工具输入日期、市场、代码或报告期错误 | tool_usage |
| tool-output-date-misread | 工具返回日期正确但链路误读 | data_asof_freshness |
| fallback-without-disclosure | 工具无数据后使用替代数据但未在答案披露 | data_asof_freshness |

## 证据要求

证据可来自 `chain[N].tools[M]` 的工具名称和输入参数、`chain[N].tools[M].output` 的日期字段。
