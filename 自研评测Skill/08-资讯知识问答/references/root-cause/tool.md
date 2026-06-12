# L1: tool

系统工具选择或执行不合理。

| L2 | 说明 | 常见受影响维度 |
|---|---|---|
| `missing_tool_call` | 明显需要检索/查询/核验却未调用工具 | `tool_usage`, `fact_evidence_quality` |
| `wrong_tool_selection` | 工具类型不匹配，如需要公司公告却只做宽泛搜索 | `tool_usage` |
| `wrong_tool_params` | 时间过滤、关键词、证券简称、项目名称或来源限制错误 | `tool_usage`, `timeliness_fact_boundary` |
| `no_cross_validation` | 单一来源下结论，未用官方/公告/新闻/纪要交叉验证 | `tool_usage`, `fact_evidence_quality` |
| `image_or_fulltext_not_used` | 需要读截图/全文/图表却只看摘要 | `tool_usage`, `nonstandard_source_awareness` |

