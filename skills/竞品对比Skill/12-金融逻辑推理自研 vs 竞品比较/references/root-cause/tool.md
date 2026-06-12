# `tool` — 工具策略

当系统工具选择、调用参数或工具编排无法支撑金融逻辑推理时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-tool-selection` | 用错工具，例如用结构化查询替代新闻/公告核验，或用搜索替代可直接取数的金融数据 | tool_usage |
| `wrong-tool-params` | 查询词、股票池、时间窗口、指标、后缀或参数不贴合任务 | tool_usage, evidence_to_conclusion |
| `missing-realtime-or-structured-check` | 短线、最新、行情、资金或财务题漏掉必要实时/结构化核验 | tool_usage, market_driver_identification |
| `missing-cross-validation` | 复杂推理只依赖单一工具或单一来源，没有交叉验证 | tool_usage, evidence_to_conclusion |
| `tool-output-not-transformed` | 工具结果不错，但最终答案没有吸收成逻辑、排序或风险判断 | tool_usage, financial_logic_chain |
| `over-fetching-no-synthesis` | 工具调用过多但没有形成清晰结论 | tool_usage, decision_value_expression |

竞品 `plan` 为空时，不要归因为“没有推理”，应基于 `chain[*].tools[*]` 的实际行为判断。
