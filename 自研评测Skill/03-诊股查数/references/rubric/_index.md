# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中建议权重仅作参考，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_fulfillment` 意图满足度 | 12 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。所有题目均考察是否回答用户真正要问的诊股/查数问题 |
| `data_accuracy_coverage` 数据准确性与覆盖 | 18 | [data_accuracy_coverage.md](data_accuracy_coverage.md) | **始终 relevant**。所有诊股查数题均需检查数据值、样本、标的、年份和字段覆盖 |
| `time_caliber_precision` 时间、口径与粒度 | 12 | [time_caliber_precision.md](time_caliber_precision.md) | **relevant**: 涉及具体日期、过去 N 年、上市以来、分时、合约、汇率、单位、复权、交易日。**supplementary**: 无明确时间口径 |
| `calculation_comparison` 计算与对比 | 10 | [calculation_comparison.md](calculation_comparison.md) | **relevant**: 涉及涨跌幅、差值、总额、比价、跑赢、排序、换算或多标的对比。**supplementary**: 简单取数 |
| `analysis_framework_fit` 市场分析框架匹配度 | 16 | [analysis_framework_fit.md](analysis_framework_fit.md) | **relevant**: 主力、筹码、增长点、止盈位、客户、商品比价、行业跑赢、诊股类问题。**supplementary**: 纯事实取数 |
| `insight_extension` 延伸洞察与增量信息 | 10 | [insight_extension.md](insight_extension.md) | **relevant**: 用户需要诊断、解释、对比、未来增长点或投资含义。**supplementary**: 简单事实查询 |
| `result_verifiability` 结果可验证性 | 8 | [result_verifiability.md](result_verifiability.md) | **relevant**: 统计、全市场筛选、历史序列、非公开/搜索补充、复杂判断。**supplementary**: 单点事实 |
| `presentation_visualization` 呈现与可视化 | 5 | [presentation_visualization.md](presentation_visualization.md) | **relevant**: 多年份、多标的、趋势对比、图表能显著提升理解。**supplementary**: 其他题目 |
| `tool_usage` 工具使用合理性 | 6 | [tool_usage.md](tool_usage.md) | **始终 relevant**。复杂诊断、跨市场、非公开资料、分时数据时提高权重 |
| `latency_efficiency` 响应耗时与执行效率 | 3 | [latency_efficiency.md](latency_efficiency.md) | **relevant**: 有耗时证据且任务简单却明显过慢，或复杂任务低效空转。**supplementary**: 有耗时但不是核心。**not_applicable**: 无耗时且极简单 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重；`supplementary` 维度保留低权重（建议 3-5）。
3. `not_applicable` 维度权重 = 0，评分阶段跳过。
4. 所有动态权重之和必须 = 100。
5. 权重分配须附简短理由。
6. 当题目落入专家案例时，案例 hard checks 可以提升相关维度权重。

## 封顶规则

- [hard_data_or_fact_error（上限 35）](cap_hard_data_or_fact_error.md)
- [missing_required_data（上限 60）](cap_missing_required_data.md)
- [time_or_caliber_error（上限 45）](cap_time_or_caliber_error.md)
- [intraday_precision_missing（上限 55）](cap_intraday_precision_missing.md)
- [wrong_analysis_framework（上限 55）](cap_wrong_analysis_framework.md)
- [data_dump_without_insight（上限 65）](cap_data_dump_without_insight.md)
- [unverifiable_or_fabricated_result（上限 50）](cap_unverifiable_or_fabricated_result.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 更好的隐藏规划不会覆盖最终答案触发的封顶规则。
- 如果答案数据正确但金融框架明显错位，例如筹码集中度只看冷门字段，应优先考虑 `wrong_analysis_framework`。
- 如果答案有图表但关键数据或口径错误，图表不构成豁免。
