# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `temporal_intent_recognition` 时间意图识别 | 15 | [temporal_intent_recognition.md](temporal_intent_recognition.md) | 任何包含相对时间、日期、周几、交易日、最新、今天、去年等表达的问题 |
| `anchor_date_resolution` 锚点日期解析 | 15 | [anchor_date_resolution.md](anchor_date_resolution.md) | 涉及今天/昨天/明天/下周/去年/年中/近N日/前N个交易日等 |
| `market_calendar_status` 交易日历状态 | 15 | [market_calendar_status.md](market_calendar_status.md) | 涉及开盘、走势、今天涨跌、港股/A股/美股/期货/外汇等 |
| `data_asof_freshness` 数据时点新鲜度 | 15 | [data_asof_freshness.md](data_asof_freshness.md) | 涉及今天为什么涨跌、最新价、最新公告、最近数据、当前行情、近期表现 |
| `period_disclosure_mapping` 财报期间映射 | 10 | [period_disclosure_mapping.md](period_disclosure_mapping.md) | 涉及去年营收、今年一季报、年中分红、某年报、最新财报、同比/环比期间 |
| `premise_correction_clarification` 前提纠错与澄清 | 10 | [premise_correction_clarification.md](premise_correction_clarification.md) | 涉及错误日期、错误星期、休市却问涨跌、上下文时间不明 |
| `answer_composition_credibility` 答案可信表达 | 10 | [answer_composition_credibility.md](answer_composition_credibility.md) | 所有时间感知题 |
| `tool_usage` 工具使用合理性 | 10 | [tool_usage.md](tool_usage.md) | 需要外部交易日历、行情、公告、财报、分红、跨市场数据或最新状态的问题 |

## 动态权重分配规则

权重总和必须为 100。按题目风险动态调整：

1. 交易日/休市/今日涨跌题：`market_calendar_status`、`data_asof_freshness`、`premise_correction_clarification` 权重最高。
2. 相对日期/周几题：`anchor_date_resolution` 权重最高，`temporal_intent_recognition` 次高。
3. 财报/分红/报告期题：`period_disclosure_mapping` 权重最高，`data_asof_freshness` 次高。
4. 最新/最近题：`data_asof_freshness` 和 `tool_usage` 权重提高。
5. 表达维度通常为 5-10；只有当主时间判断正确但用户仍可能误解时才提高。
6. `not_applicable` 维度权重为 0，不进入 `dimension_scores`。

## 封顶规则

- [hard_wrong_anchor_date（上限 40）](cap_hard_wrong_anchor_date.md)
- [market_closed_answered_as_open（上限 35）](cap_market_closed_answered_as_open.md)
- [stale_data_masquerading_as_today（上限 45）](cap_stale_data_masquerading_as_today.md)
- [missing_required_premise_correction（上限 50）](cap_missing_required_premise_correction.md)
- [fiscal_period_disclosure_error（上限 50）](cap_fiscal_period_disclosure_error.md)
- [fabricated_time_fact（上限 30）](cap_fabricated_time_fact.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 如果多条封顶规则同时触发，取最低的分数上限。
