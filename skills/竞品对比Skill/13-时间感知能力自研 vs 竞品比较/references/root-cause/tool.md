# tool

系统是否选对工具、填对日期/市场/代码/报告期，并正确读取工具返回的时间字段。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| calendar-tool-missing | 应查交易日历、行情日历或市场状态但未调用 | tool_usage |
| wrong-tool-date-input | 工具输入日期、市场、代码或报告期错误 | tool_usage |
| tool-output-date-misread | 工具返回日期正确但链路误读 | data_asof_freshness |
| fallback-without-disclosure | 工具无数据后使用替代数据但未在答案披露 | data_asof_freshness |

## 比较使用

不要按工具数量判断胜负。只比较工具是否支撑本题最关键的时间判断，并最终改善了答案。
