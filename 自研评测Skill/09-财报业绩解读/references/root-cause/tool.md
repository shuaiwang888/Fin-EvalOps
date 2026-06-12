# `tool` — 选择与执行工具

当系统因为工具选择、查询方式或验证链路错误导致答案质量下降时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `structured-only-no-fulltext` | 只用 FinQuery 等结构化财务字段，未查公告全文或公司原文 | tool_usage, primary_evidence_quality |
| `wrong-tool-for-disclosure` | 用 Search 摘要或结构化数据替代应读取的年报附注、季报说明、分红公告或官网公告 | tool_usage, primary_evidence_quality |
| `poor-financial-query-formulation` | 查询词缺少公司名、报告期、公告类型、会计事件或关键科目，导致召回不准 | tool_usage, report_data_accuracy |
| `fulltext-fetch-failed-not-recovered` | 全文获取失败后没有换关键词、换公告名或换来源验证 | tool_usage, primary_evidence_quality |
| `cross-validation-missing` | 财务数据、公告原文、行业背景、行情反应之间没有交叉验证 | tool_usage, business_financial_linkage |
| `calculation-tool-missed` | 差额闭合、敏感度、估值对比、占比计算等需要测算时未做清晰计算 | tool_usage, report_data_accuracy |
| `inefficient-tool-chain` | 多轮低效搜索或重复查询，耗时增加但没有获得关键证据 | tool_usage, composition_credibility |
