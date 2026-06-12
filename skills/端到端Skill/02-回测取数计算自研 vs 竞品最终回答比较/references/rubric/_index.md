# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `intent_fulfillment` 意图满足度 | 13 | [intent_fulfillment.md](intent_fulfillment.md) | **始终 relevant**。所有题目均考察取数计算需求是否被满足 |
| `data_retrieval_accuracy` 取数准确性 | 23 | [data_retrieval_accuracy.md](data_retrieval_accuracy.md) | **始终 relevant**。所有取数计算题目均需考察数据正确性和覆盖完整性 |
| `time_inference` 时间推理正确性 | 17 | [time_inference.md](time_inference.md) | **relevant**: 涉及具体日期/交易日/节假日倒推/时间范围。**supplementary**: 无明确时间推理 |
| `calculation_accuracy` 计算准确性 | 18 | [calculation_accuracy.md](calculation_accuracy.md) | **relevant**: 涉及涨跌幅/概率/盈亏/衍生指标计算。**supplementary**: 以数据提取为主 |
| `logical_decomposition` 逻辑拆解能力 | 10 | [logical_decomposition.md](logical_decomposition.md) | **relevant**: 多步/多条件复合查询。**supplementary**: 单步查询拆解。**not_applicable**: 简单单步取数 |
| `result_verifiability` 结果可验证性 | 12 | [result_verifiability.md](result_verifiability.md) | **relevant**: 统计概率/历史回测需逐条明细。**supplementary**: 单次计算 |
| `expression_quality` 表达与展示质量 | 7 | [expression_quality.md](expression_quality.md) | **始终 supplementary**。表达质量有参考价值但优先级低于正确性 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，从 `not_applicable` 或低相关维度让出权重。
3. `supplementary` 维度保留低权重，通常 3-10。
4. `not_applicable` 维度权重 = 0，评分阶段跳过。
5. 所有动态权重之和必须 = 100。
6. 权重分配须附简短理由，记录在输出的 `weight_assignment[*].rationale` 中。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接完成用户要求的取数、统计、回测或计算任务。
- 数据值、字段、样本、筛选范围和标的范围是否正确完整。
- 交易日、节假日、盘中时点、披露日、上市以来和统计区间是否准确。
- 公式、算术、分子分母、单位换算、复权口径和统计口径是否正确。
- 多步任务是否拆解为条件发现、信号生成、买卖动作、收益计算或阈值筛选。
- 关键结论是否有明细、样本量、中间值和公式代入支撑。
- 数据密集型答案是否结构清楚，表格、口径和结论是否便于复核。
- 是否避免用少量示例冒充全市场、全历史或长期概率统计。
- 无法取得完整数据时，是否明确说明局限而不是编造精确结果。

## 质量标签

- [data_fabrication](cap_data_fabrication.md)
- [time_inference_error](cap_time_inference_error.md)
- [calculation_logic_error](cap_calculation_logic_error.md)
- [intraday_precision_missing](cap_intraday_precision_missing.md)
- [missing_required_data](cap_missing_required_data.md)
- [unverifiable_result](cap_unverifiable_result.md)

## 质量标签注意事项

- 质量标签记录在 `applied_caps`，只作为 hard check 命中说明。
- 质量标签不替代维度评分；触发标签后仍需完成逐维评分。
- 质量标签只能依据最终回答文本触发。
- 标签对应的 `ceiling` 和最终分处理由调用方代码根据 `scripts/rule.py` 完成。

## 维度边界区分

- `data_retrieval_accuracy` vs `calculation_accuracy`：基础数据字段、样本和价格取错扣 `data_retrieval_accuracy`；公式选择、算术、分子分母、复权收益方法错误扣 `calculation_accuracy`。
- `time_inference` vs `data_retrieval_accuracy`：时间窗口、交易日、披露日、盘中时点推错扣 `time_inference`；时间正确但取到的数据字段或样本不全扣 `data_retrieval_accuracy`。
- `logical_decomposition` vs `result_verifiability`：复合任务没有拆成可执行子步骤扣 `logical_decomposition`；步骤可能存在但最终回答缺少明细和中间过程扣 `result_verifiability`。
- `result_verifiability` vs `expression_quality`：缺少可复核数据和公式扣 `result_verifiability`；有足够信息但组织混乱、表格差、重点不清扣 `expression_quality`。
