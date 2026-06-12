# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `intent_fulfillment` 意图满足度 | 13 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。所有题目均考察取数计算需求是否被满足 |
| `data_retrieval_accuracy` 取数准确性 | 20 | [data_retrieval_accuracy.md](data_retrieval_accuracy.md) | **始终 relevant**。所有取数计算题目均需考察数据正确性和覆盖完整性 |
| `time_inference` 时间推理正确性 | 15 | [time_inference.md](time_inference.md) | **relevant**: 涉及具体日期/交易日/节假日倒推/时间范围。**supplementary**: 无明确时间推理 |
| `calculation_accuracy` 计算准确性 | 15 | [calculation_accuracy.md](calculation_accuracy.md) | **relevant**: 涉及涨跌幅/概率/盈亏/衍生指标计算。**supplementary**: 以数据提取为主 |
| `logical_decomposition` 逻辑拆解能力 | 10 | [logical_decomposition.md](logical_decomposition.md) | **relevant**: 多步/多条件复合查询。**supplementary**: 单步查询拆解。**not_applicable**: 简单单步取数 |
| `result_verifiability` 结果可验证性 | 10 | [result_verifiability.md](result_verifiability.md) | **relevant**: 统计概率/历史回测需逐条明细。**supplementary**: 单次计算 |
| `expression_quality` 表达与展示质量 | 7 | [expression_quality.md](expression_quality.md) | **始终 supplementary**。表达质量有参考价值但优先级低于正确性 |
| `tool_usage` 工具使用合理性 | 5 | [tool_usage.md](tool_usage.md) | **始终 relevant**。但权重通常较低（建议 3-5），除非涉及复杂多步工具编排 |
| `latency_efficiency` 响应耗时与执行效率 | 5 | [latency_efficiency.md](latency_efficiency.md) | **relevant**: 大规模统计/全市场筛选且有耗时证据。**supplementary**: 简单任务或无耗时证据。**not_applicable**: 极简单查询 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`
2. `relevant` 维度获得较高权重（从 `not_applicable` 维度让出权重）
3. `supplementary` 维度保留低权重（建议 3-5）
4. `not_applicable` 维度权重 = 0，评分阶段跳过
5. 所有动态权重之和必须 = 100
6. 权重分配须附简短理由（记录在输出的 `weight_assignment[*].rationale` 中）

## 封顶规则

- data_fabrication（上限 35）
- time_inference_error（上限 45）
- calculation_logic_error（上限 50）
- intraday_precision_missing（上限 55）
- missing_required_data（上限 60）
- unverifiable_result（上限 65）

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 更好的隐藏规划不会覆盖最终答案触发的封顶规则。
- 仅检查与 `relevant`/`supplementary` 维度相关的封顶规则。
