# 评分细则索引

## 维度池

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_condition_extraction` 意图与条件抽取 | 18 | [intent_condition_extraction.md](intent_condition_extraction.md) | **始终 relevant**。复杂选股首先看条件是否被完整保留 |
| `financial_semantics_and_caliber` 金融语义与口径 | 14 | [financial_semantics_and_caliber.md](financial_semantics_and_caliber.md) | **relevant**：涉及指标公式、资金流、龙虎榜、北向、ST/退市、主线题材等 |
| `screening_plan_decomposition` 筛选规划拆解 | 14 | [screening_plan_decomposition.md](screening_plan_decomposition.md) | **relevant**：长问句、多阶段、二次验证、前后依赖、跨领域筛选 |
| `tool_usage` 工具与信源匹配 | 12 | [tool_usage.md](tool_usage.md) | **始终 relevant**，在链路诊断阶段评分 |
| `result_correctness_and_coverage` 结果正确性与覆盖 | 16 | [result_correctness_and_coverage.md](result_correctness_and_coverage.md) | **始终 relevant**。最终候选池、字段、无结果说明是否可用 |
| `ranking_and_decision_actionability` 排序与决策可执行性 | 10 | [ranking_and_decision_actionability.md](ranking_and_decision_actionability.md) | **relevant**：用户要求排序、Top N、选一只、候选池或仅显示指定字段 |
| `data_logic_time_boundary` 数据逻辑与时间边界 | 10 | [data_logic_time_boundary.md](data_logic_time_boundary.md) | **relevant**：涉及日期、交易日、分时、K 线、回撤、涨跌幅区间、公式 |
| `composition_credibility` 表达可信度 | 6 | [composition_credibility.md](composition_credibility.md) | **supplementary**：所有题目都有表达可信度要求 |

## 动态权重分配规则

1. 活跃维度权重总和必须为 100。
2. 长问句和条件很多时，提高 `intent_condition_extraction` 与 `screening_plan_decomposition`。
3. 指标公式、资金、北向、龙虎榜、退市风险等口径复杂时，提高 `financial_semantics_and_caliber` 与 `data_logic_time_boundary`。
4. 含主线题材、合作关系、订单、极端利好、核心技术等非标条件时，提高 `tool_usage`。
5. 用户要求排序、Top N、选一只或候选池时，提高 `ranking_and_decision_actionability`。
6. 输出无结果或候选池很少时，提高 `result_correctness_and_coverage`，重点检查条件是否被过度收紧或误解析。

## 封顶规则

- [core_condition_omitted_or_rewritten（上限 45）](cap_core_condition_omitted_or_rewritten.md)
- [hard_financial_semantics_or_caliber_error（上限 45）](cap_hard_financial_semantics_or_caliber_error.md)
- [unsupported_data_forced_output（上限 50）](cap_unsupported_data_forced_output.md)
- [wrong_tool_strategy（上限 55）](cap_wrong_tool_strategy.md)
- [layered_or_temporal_screening_failure（上限 55）](cap_layered_or_temporal_screening_failure.md)
- [missing_required_ranking_or_fields（上限 60）](cap_missing_required_ranking_or_fields.md)
- [unverifiable_result_or_data_hallucination（上限 50）](cap_unverifiable_result_or_data_hallucination.md)
- [chart_or_table_without_decision_value（上限 65）](cap_chart_or_table_without_decision_value.md)

封顶限制最终分数，不替代维度评分。隐藏规划更好不能覆盖最终答案触发的封顶。
