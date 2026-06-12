# `tool` — 选择与执行工具

当规划链路选错工具、误用工具或违反工具约束时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-tool-selection` | 用 Search 查 FinQuery 能处理的结构化数据，用 FinQuery 查需 Search 的非结构化背景，或查最新资讯/公告时未使用 Search 并加正确后缀（"新闻"、"公告"、"研报"） | industry_mapping, timeliness_fact_boundary, tool_usage |
| `tool-input-error` | 遗漏工具后缀，单次 FinQuery 过载，或未合并可合并的查询条件 | industry_mapping, timeliness_fact_boundary, tool_usage |
| `tool-constraint-violation` | 需要数据处理或科学计算时未使用 CodeInterpreter，或 CodeInterpreter 输入非 Python 代码 | tool_usage |
| `missing-tool-combination` | 需要 Search/AccessingFullText 获取产业事实，再用 FinQuery/BackTest 补行情财务时，只用了单一工具导致证据缺口 | tool_usage, logic_closure |
| `source-conflict-unresolved` | FinQuery、搜索、公告、异动提醒或年报等来源口径冲突，但未核验也未解释，直接拼接为答案 | tool_usage, credibility_expression |
