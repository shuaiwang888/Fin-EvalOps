# 评分细则索引

## 先拆复合任务，不先套题型

复合意图类问题要先判断用户一句话里包含哪些子任务，以及这些子任务之间的依赖关系。评测重点不是“写得多不多”，而是“拆得准、答得全、证据能支撑、结论能落地”。

步骤：
1. 从 `question` 和必要 `context` 抽取子任务清单：取数、新闻/公告、行业/政策、财务/估值、案例比较、影响评估、传导路径、策略建议、交易方案等。
2. 标注主任务和辅助任务，判断哪些遗漏会改变用户最终决策。
3. 判断证据需求：时间窗口、数据口径、对比对象、量化指标、案例真实性、工具需求。
4. 从下方维度池选择适用维度；当线上数据暴露的关键缺口不能被现有维度清楚覆盖时，可新增临时评分维度，并直接并入 `weight_assignment` 与 `dimension_scores`。

## 维度池

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_decomposition` 意图拆解 | 16 | [intent_decomposition.md](intent_decomposition.md) | **始终 relevant** |
| `task_coverage_priority` 子任务覆盖与主次 | 14 | [task_coverage_priority.md](task_coverage_priority.md) | **始终 relevant** |
| `multi_source_evidence_integration` 多源证据整合 | 14 | [multi_source_evidence_integration.md](multi_source_evidence_integration.md) | **relevant**: 涉及行情、新闻、公告、产业、政策、财务、资金等多源信息 |
| `analysis_chain_closure` 分析链路闭环 | 16 | [analysis_chain_closure.md](analysis_chain_closure.md) | **始终 relevant** |
| `data_logic_rigor` 数据与逻辑严谨性 | 14 | [data_logic_rigor.md](data_logic_rigor.md) | **relevant**: 涉及计算、回撤、估值、利润、案例、时间窗口、量化对比 |
| `decision_actionability` 决策表达与可执行性 | 10 | [decision_actionability.md](decision_actionability.md) | **relevant**: 用户要求策略、择股、布局、调仓、合约、价位、操作框架 |
| `composition_readability` 结构与可读性 | 5 | [composition_readability.md](composition_readability.md) | **始终 supplementary** |
| `tool_usage` 工具使用合理性 | 7 | [tool_usage.md](tool_usage.md) | **始终 relevant**，在链路诊断阶段评分 |

## 动态权重分配规则

1. 所有活跃维度 `dynamic_weight` 之和必须 = 100。
2. 多子任务和长问句提高 `intent_decomposition`、`task_coverage_priority` 权重。
3. 涉及历史数据、估值、利润、回撤、案例先例、合约价位时，提高 `data_logic_rigor` 权重。
4. 涉及新闻、公告、政策、舆论、产业、财务等多源材料时，提高 `multi_source_evidence_integration` 和 `tool_usage` 权重。
5. 用户明确要求“影响、传导、策略、怎么做、哪个最好”时，提高 `analysis_chain_closure` 和 `decision_actionability` 权重。

## 封顶规则

- [missed_major_subtask（上限 65）](cap_missed_major_subtask.md)
- [data_or_case_unreliable（上限 55）](cap_data_or_case_unreliable.md)
- [calculation_or_time_window_error（上限 55）](cap_calculation_or_time_window_error.md)
- [information_pile_without_synthesis（上限 60）](cap_information_pile_without_synthesis.md)
- [missing_required_decision_output（上限 65）](cap_missing_required_decision_output.md)
- [wrong_or_shallow_evidence_mix（上限 60）](cap_wrong_or_shallow_evidence_mix.md)

封顶限制最终分数，不替代维度评分。更好的隐藏规划不能覆盖最终答案触发的封顶。

## 截图专家锚点

当题目命中 10 个专家样例，或输入里带有问财/豆包原始输出截图、OCR、人工批注时，读取 [../golden_cases/image_output_anchors.md](../golden_cases/image_output_anchors.md)。这些锚点优先用于校准以下高频误判：
- 把月内最大回撤、事件后交易日、48 小时/7 天窗口等关键口径算错。
- 用报告式结构和大量表格掩盖数据、案例或资金流错误。
- 回答覆盖了背景，却漏掉用户后半句的强子任务。
- 给出热点、策略、合约和价位，但没有可执行触发条件、盈亏公式或风险边界。
