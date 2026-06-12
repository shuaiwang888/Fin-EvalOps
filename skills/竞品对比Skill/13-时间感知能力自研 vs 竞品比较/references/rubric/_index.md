# 时间感知评分细则索引

本目录沿用第 13 类时间感知能力 self_judge 的维度、动态权重和封顶规则。比较评测只增加双边同题共享权重和 pairwise 输出要求，不改变以下评测维度本身。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中建议权重仅作参考基准，实际权重由步骤 0 的时间锚点分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `temporal_intent_recognition` 时间意图识别 | 15 | [temporal_intent_recognition.md](temporal_intent_recognition.md) | 包含相对时间、日期、周几、交易日、最新、今年/去年、截至等表达时 relevant |
| `anchor_date_resolution` 锚定日期解析 | 15 | [anchor_date_resolution.md](anchor_date_resolution.md) | 今天/昨天/明天/下周/去年/年中/近 N 日/前 N 个交易日等问题 relevant |
| `market_calendar_status` 市场交易日历状态 | 15 | [market_calendar_status.md](market_calendar_status.md) | 涉及开盘、走势、涨跌、休市、市场/品种交易状态时 relevant |
| `data_asof_freshness` 数据时点与新鲜度 | 15 | [data_asof_freshness.md](data_asof_freshness.md) | 涉及今天、最新、最近、当前行情、公告、价格或近期表现时 relevant |
| `period_disclosure_mapping` 报告期与披露期映射 | 10 | [period_disclosure_mapping.md](period_disclosure_mapping.md) | 涉及财报、分红、年度/季度/年中、同比/环比期间时 relevant |
| `premise_correction_clarification` 时间前提纠错与澄清 | 10 | [premise_correction_clarification.md](premise_correction_clarification.md) | 用户问题含错误日期、错误星期、休市却问涨跌、未来不可知或上下文时间不明时 relevant |
| `answer_composition_credibility` 答案组织与可信边界 | 10 | [answer_composition_credibility.md](answer_composition_credibility.md) | 所有时间感知题均适用，通常为 supplementary |
| `tool_usage` 工具使用合理性 | 10 | [tool_usage.md](tool_usage.md) | 需要外部交易日历、行情、公告、财报、分红、跨市场数据或最新状态时 relevant |

## 动态权重分配规则

权重总和必须为 100。按题目风险动态调整：

- 交易日/休市/今日涨跌题：`market_calendar_status`、`data_asof_freshness`、`premise_correction_clarification` 权重最高。
- 相对日期/周几题：`anchor_date_resolution` 权重最高，`temporal_intent_recognition` 次高。
- 财报/分红/报告期题：`period_disclosure_mapping` 权重最高，`data_asof_freshness` 次高。
- 最新/最近题：`data_asof_freshness` 和 `tool_usage` 权重提高。
- 表达维度通常为 5-10；只有当主时间判断正确但用户仍可能误解时才提高。
- `not_applicable` 维度权重为 0，不进入 `dimension_scores`。
- 自研和竞品必须使用同一套适用性与权重。

## 封顶规则

- [hard_wrong_anchor_date 核心日期锚点错误（上限 40）](cap_hard_wrong_anchor_date.md)
- [market_closed_answered_as_open 休市日按开盘回答（上限 35）](cap_market_closed_answered_as_open.md)
- [stale_data_masquerading_as_today 旧数据冒充今天/最新（上限 45）](cap_stale_data_masquerading_as_today.md)
- [missing_required_premise_correction 缺失必要前提纠错（上限 50）](cap_missing_required_premise_correction.md)
- [fiscal_period_disclosure_error 财报/分红/报告期映射错误（上限 50）](cap_fiscal_period_disclosure_error.md)
- [fabricated_time_fact 编造时间事实（上限 30）](cap_fabricated_time_fact.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 更好的隐藏规划不会覆盖最终答案触发的封顶规则。
- 同一答案同时触发多条封顶时取最低上限。
- 同题比较中，封顶规则对自研和竞品按同一标准独立触发。
