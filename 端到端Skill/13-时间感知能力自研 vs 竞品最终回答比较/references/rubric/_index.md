# 时间感知评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“建议权重”是 result-only 回退权重，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `temporal_intent_recognition` 时间意图识别 | 15 | [temporal_intent_recognition.md](temporal_intent_recognition.md) | 包含相对时间、日期、周几、交易日、最新、今天、去年、年中、截至等表达时 relevant |
| `anchor_date_resolution` 锚定日期解析 | 15 | [anchor_date_resolution.md](anchor_date_resolution.md) | 今天/昨天/明天/下周/去年/年中/近 N 日/前 N 个交易日等问题 relevant |
| `market_calendar_status` 市场交易日历状态 | 18 | [market_calendar_status.md](market_calendar_status.md) | 涉及开盘、走势、涨跌、休市、市场/品种交易状态时 relevant |
| `data_asof_freshness` 数据时点与新鲜度 | 18 | [data_asof_freshness.md](data_asof_freshness.md) | 涉及今天、最新、最近、当前行情、公告、价格或近期表现时 relevant |
| `period_disclosure_mapping` 报告期与披露期映射 | 10 | [period_disclosure_mapping.md](period_disclosure_mapping.md) | 涉及财报、分红、年度/季度/年中、同比/环比期间时 relevant |
| `premise_correction_clarification` 时间前提纠错与澄清 | 12 | [premise_correction_clarification.md](premise_correction_clarification.md) | 用户问题含错误日期、错误星期、休市却问涨跌、未来不可知或上下文时间不明时 relevant |
| `answer_composition_credibility` 答案组织与可信边界 | 12 | [answer_composition_credibility.md](answer_composition_credibility.md) | 所有时间感知题均适用，通常为 supplementary |

## 动态权重分配规则

1. 仅阅读用户问题和可见请求时间，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 权重 = 0。
3. 权重总和必须 = 100。
4. 决策任务不同，权重可调整：
   - 交易日/休市/今日涨跌题：提高 `market_calendar_status`、`data_asof_freshness`、`premise_correction_clarification`；
   - 相对日期/周几题：提高 `anchor_date_resolution`，并保留 `temporal_intent_recognition`；
   - 财报/分红/报告期题：提高 `period_disclosure_mapping` 和 `data_asof_freshness`；
   - 最新/最近题：提高 `data_asof_freshness` 和 `answer_composition_credibility`；
   - 用户时间前提明显错误题：提高 `premise_correction_clarification`。
5. 权重分配须附简短理由（记录在输出的 `weight_assignment[*].rationale` 中）。

## 封顶规则

- [hard_wrong_anchor_date 核心日期锚点错误（标签上限 40）](cap_hard_wrong_anchor_date.md)
- [market_closed_answered_as_open 休市日按开盘回答（标签上限 35）](cap_market_closed_answered_as_open.md)
- [stale_data_masquerading_as_today 旧数据冒充今天/最新（标签上限 45）](cap_stale_data_masquerading_as_today.md)
- [missing_required_premise_correction 缺失必要前提纠错（标签上限 50）](cap_missing_required_premise_correction.md)
- [fiscal_period_disclosure_error 财报/分红/报告期映射错误（标签上限 50）](cap_fiscal_period_disclosure_error.md)
- [fabricated_time_fact 编造时间事实（标签上限 30）](cap_fabricated_time_fact.md)

## 封顶规则注意事项

- 封顶规则在本 result-only skill 中作为质量标签记录在 `applied_caps`，不直接改写分数。
- 标签不替代维度评分；同一问题仍需完成所有活跃维度评分。
- 同一最终回答同时触发多条封顶标签时，全部记录。
- 同题比较中，封顶标签对自研和竞品按同一标准独立触发。
