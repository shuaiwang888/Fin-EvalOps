# L1: `evidence`

用于归因推荐缺少必要证据，或证据不能支撑结论。

常见 L2：
- `missing-required-market-data`：用户要求历史表现、估值分位、盈利确定性、资金面等，答案未给关键数据。
- `shallow-source-for-recommendation`：用浅层资讯、概念描述或旧消息支撑投资建议。
- `evidence-not-linked-to-action`：数据很多，但没有说明如何推导仓位、标的或取舍。
- `wrong-evidence-granularity`：中长期配置用短线技术指标，短线交易缺少当下盘面和流动性证据。

证据要求：
- 引用用户要求的证据类型。
- 引用最终答案中证据缺失、浅层或断裂的位置。
- 如工具链有输出，引用工具结果与最终答案的关系。
