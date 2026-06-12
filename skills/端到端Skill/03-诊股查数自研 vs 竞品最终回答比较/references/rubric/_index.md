# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“默认权重”是 result-only 基准权重；实际权重可按题目适用性调整，但双方必须使用同一套权重且总和为 100。

| 维度 | 默认权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_fulfillment` 意图满足度 | 12 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。所有题目均考察是否回答用户真正要问的诊股/查数问题 |
| `data_accuracy_coverage` 数据准确性与覆盖 | 20 | [data_accuracy_coverage.md](data_accuracy_coverage.md) | **始终 relevant**。所有诊股查数题均需检查数据值、样本、标的、年份和字段覆盖 |
| `time_caliber_precision` 时间、口径与粒度 | 13 | [time_caliber_precision.md](time_caliber_precision.md) | **relevant**: 涉及具体日期、过去 N 年、上市以来、分时、合约、汇率、单位、复权、交易日。**supplementary**: 无明确时间口径 |
| `calculation_comparison` 计算与对比 | 11 | [calculation_comparison.md](calculation_comparison.md) | **relevant**: 涉及涨跌幅、差值、总额、比价、跑赢、排序、换算或多标的对比。**supplementary**: 简单取数 |
| `analysis_framework_fit` 市场分析框架匹配度 | 18 | [analysis_framework_fit.md](analysis_framework_fit.md) | **relevant**: 主力、筹码、增长点、止盈位、客户、商品比价、行业跑赢、诊股类问题。**supplementary**: 纯事实取数 |
| `insight_extension` 延伸洞察与增量信息 | 11 | [insight_extension.md](insight_extension.md) | **relevant**: 用户需要诊断、解释、对比、未来增长点或投资含义。**supplementary**: 简单事实查询 |
| `result_verifiability` 结果可验证性 | 10 | [result_verifiability.md](result_verifiability.md) | **relevant**: 统计、全市场筛选、历史序列、非公开/搜索补充、复杂判断。**supplementary**: 单点事实 |
| `presentation_visualization` 呈现与可视化 | 5 | [presentation_visualization.md](presentation_visualization.md) | **relevant**: 多年份、多标的、趋势对比、图表能显著提升理解。**supplementary**: 其他题目 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重；`supplementary` 维度保留低权重。
3. `not_applicable` 维度权重为 0，评分阶段跳过。
4. 所有动态权重之和必须为 100。
5. 权重分配须附简短理由。
6. 当题目落入专家案例时，案例 hard checks 可以提升相关维度权重。

## 质量标签

以下标签只记录最终回答命中的严重质量问题。LLM 输出 `applied_caps` 与最终回答证据；`ceiling`、限分和总分计算由代码根据 `scripts/rule.py` 处理。

- [hard_data_or_fact_error](cap_hard_data_or_fact_error.md)：硬性数据/事实错误
- [missing_required_data](cap_missing_required_data.md)：必要数据缺失
- [time_or_caliber_error](cap_time_or_caliber_error.md)：时间/口径错误
- [intraday_precision_missing](cap_intraday_precision_missing.md)：日内精度缺失
- [wrong_analysis_framework](cap_wrong_analysis_framework.md)：分析框架错误
- [data_dump_without_insight](cap_data_dump_without_insight.md)：数据堆砌无洞察
- [unverifiable_or_fabricated_result](cap_unverifiable_or_fabricated_result.md)：不可验证或疑似编造

## 质量标签注意事项

- 质量标签不替代维度评分。
- 标签必须由最终回答文本直接支持，不能根据过程信息推断。
- 如果答案数据正确但金融框架明显错位，例如筹码集中度只看冷门字段，应优先考虑 `wrong_analysis_framework`。
- 如果答案有图表但关键数据或口径错误，图表不构成豁免。
- 如果答案给出精确客户、订单、资金流、统计结果或排名，但缺少可复核明细，应考虑 `unverifiable_or_fabricated_result`。

## 证据边界

证据只能来自：
- 用户问题；
- 自研最终回答；
- 竞品最终回答。

不得引用或评价任何过程字段。
