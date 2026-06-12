# `tool` — 选择与执行工具

当规划链路选错工具、输入不合适、漏用必要工具或没有处理工具失败时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-tool-selection` | 用 Search 查结构化行情/财务，或用 FinQuery 查非结构化新闻/政策/研报背景 | tool_usage, evidence_source_quality |
| `tool-input-error` | 工具输入遗漏关键约束、后缀、日期、标的、指标，或改写了用户条件 | tool_usage, intent_scenario_recognition |
| `missing-recency-search` | 最新消息、行情归因、题材发酵问题没有检索最新新闻、公告或政策 | tool_usage, recency_time_boundary |
| `missing-deep-read` | 搜到网页、公告、研报线索但没有用 AccessingFullText 深读关键内容 | tool_usage, evidence_source_quality |
| `tool-failure-not-validated` | 工具返回 0 条、异常或口径不确定后，未验证就直接下结论 | tool_usage, evidence_source_quality |
| `calculation-tool-omitted` | 需要历史分位、回撤、排名、占比、统计计算时未使用合适计算能力 | tool_usage, comparison_quantification |
| `missing-user-profile-lookup` | 个人化推荐或持仓决策问题没有读取、检索或利用可见用户画像、历史上下文或画像工具 | tool_usage, user_profile_suitability |

证据优先看 `chain.plan`、`chain.tools[M].input` 和 `chain.tools[M].output`。
