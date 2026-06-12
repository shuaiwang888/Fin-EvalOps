# `tool` — 选择与执行工具

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `entity-disambiguation-failed` | 工具返回多个相似实体后未消歧 | entity_product_boundary, tool_usage |
| `wrong-tool-for-caliber` | 用不适合的工具获取指标、盘中价或报告期 | metric_caliber_accuracy, tool_usage |
| `tool-output-overtrusted` | 未审查工具结果是否符合金融常识 | financial_term_understanding, tool_usage |
| `missing-realtime-check` | 需要盘中/最新数据但没有实时核验 | timeliness_context, tool_usage |
