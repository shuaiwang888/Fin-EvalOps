# `capability_gap` — 数据源或能力缺口

当当前工具或数据源客观缺少完成题目所需的专业资料，且该缺口解释了答案质量下降时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `missing-specialized-source` | 缺少调研纪要、研报全文、iFind/专业数据库、知识星球等来源 | evidence_source_quality, tool_usage |
| `insufficient-real-time-feed` | 金融实时资讯要求很高，当前搜索或数据刷新无法满足分钟级信息需求 | recency_time_boundary, evidence_source_quality |
| `missing-user-portfolio-context` | 需要结合用户持仓、风险偏好、交易风格，但输入或工具没有提供；仅在链路已合理尝试获取画像后使用 | user_profile_suitability, actionability_risk |
| `unsupported-private-data` | 客户占比、供应链份额、订单比例等没有公开稳定数据源 | evidence_source_quality |

使用要求：
- 不能用 `capability_gap` 为模型偷懒开脱。只有当链路已经合理尝试，且确实需要外部专业资料时才使用。
- 若模型没有尝试必要工具，优先归因 `tool`。
- 若工具可查但没查到关键资料，优先归因 `evidence` 或 `tool`。
