# 评分细则索引

## 先拆复合任务，不先套题型

复合意图类问题要先判断用户一句话里包含哪些子任务，以及这些子任务之间的依赖关系。评测重点不是“写得多不多”，而是“拆得准、答得全、证据能支撑、结论能落地”。

步骤：
1. 仅从 `question` 抽取子任务清单：取数、新闻/公告、行业/政策、财务/估值、案例比较、影响评估、传导路径、策略建议、交易方案等。
2. 标注主任务和辅助任务，判断哪些遗漏会改变用户最终决策。
3. 判断证据需求：时间窗口、数据口径、对比对象、量化指标、案例真实性和决策输出。
4. 从下方维度池选择适用维度，并为双方使用同一套权重。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“默认权重”是 result-only 基准权重；实际权重可按题目适用性调整，但双方必须使用同一套权重且总和为 100。

| 维度 | 默认权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `intent_decomposition` 意图拆解 | 16 | [intent_decomposition.md](intent_decomposition.md) | **始终 relevant**。所有复合意图题均需判断子任务、时间窗口、对象和输出要求 |
| `task_coverage_priority` 子任务覆盖与主次 | 15 | [task_coverage_priority.md](task_coverage_priority.md) | **始终 relevant**。必须覆盖关键子任务并按用户决策价值排序 |
| `multi_source_evidence_integration` 多源证据整合 | 16 | [multi_source_evidence_integration.md](multi_source_evidence_integration.md) | **relevant**: 涉及行情、新闻、公告、产业、政策、财务、资金等多源信息。**supplementary**: 单一计算或单一交易方案 |
| `analysis_chain_closure` 分析链路闭环 | 18 | [analysis_chain_closure.md](analysis_chain_closure.md) | **始终 relevant**。复合任务必须形成事实、影响、传导、策略或结论闭环 |
| `data_logic_rigor` 数据与逻辑严谨性 | 17 | [data_logic_rigor.md](data_logic_rigor.md) | **relevant**: 涉及计算、回撤、估值、利润、案例、时间窗口、量化对比。**supplementary**: 纯框架讨论 |
| `decision_actionability` 决策表达与可执行性 | 13 | [decision_actionability.md](decision_actionability.md) | **relevant**: 用户要求策略、择股、布局、调仓、合约、价位、操作框架。**supplementary**: 研究理解 |
| `composition_readability` 结构与可读性 | 5 | [composition_readability.md](composition_readability.md) | **始终 supplementary**。复杂问题需要清晰结构降低理解成本 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. `relevant` 维度获得较高权重，`supplementary` 维度保留低权重，`not_applicable` 维度权重为 0。
3. 所有活跃维度的 `dynamic_weight` 之和必须为 100。
4. 多子任务和长问句提高 `intent_decomposition`、`task_coverage_priority` 权重。
5. 涉及历史数据、估值、利润、回撤、案例先例、合约价位时，提高 `data_logic_rigor` 权重。
6. 涉及新闻、公告、政策、舆论、产业、财务等多源材料时，提高 `multi_source_evidence_integration` 权重。
7. 用户明确要求“影响、传导、策略、怎么做、哪个最好”时，提高 `analysis_chain_closure` 和 `decision_actionability` 权重。

## 质量标签

以下标签只记录最终回答命中的严重质量问题。LLM 输出 `applied_caps` 与最终回答证据；`ceiling`、限分和总分计算由代码根据 `scripts/rule.py` 处理。

- [missed_major_subtask](cap_missed_major_subtask.md)：遗漏主要子任务
- [data_or_case_unreliable](cap_data_or_case_unreliable.md)：数据或案例不可靠
- [calculation_or_time_window_error](cap_calculation_or_time_window_error.md)：计算或时间窗口错误
- [information_pile_without_synthesis](cap_information_pile_without_synthesis.md)：信息堆砌无综合
- [missing_required_decision_output](cap_missing_required_decision_output.md)：遗漏必要决策输出
- [wrong_or_shallow_evidence_mix](cap_wrong_or_shallow_evidence_mix.md)：证据组合错误或浅层

## 质量标签注意事项

- 质量标签不替代维度评分。
- 标签必须由最终回答文本直接支持，不能根据过程信息推断。
- 关键子任务漏答、数据/案例失真、时间窗口错配、资料拼盘无综合、缺少决策输出，是复合意图类答案的高优先级硬伤。
- 表格完整、标题清楚、引用数量多，不足以抵消关键数据、案例、口径或时间窗口错误。

## 专家锚点

当题目命中 10 个专家样例或同类任务结构时，读取 [../golden_cases/image_output_anchors.md](../golden_cases/image_output_anchors.md)。这些锚点优先用于校准以下高频误判：
- 把月内最大回撤、事件后交易日、48 小时/7 天窗口等关键口径算错。
- 用报告式结构和大量表格掩盖数据、案例或资金流错误。
- 回答覆盖了背景，却漏掉用户后半句的强子任务。
- 给出热点、策略、合约和价位，但没有可执行触发条件、盈亏公式或风险边界。

## 证据边界

证据只能来自：
- 用户问题；
- 自研最终回答；
- 竞品最终回答。

不得引用或评价任何过程字段、上下文字段或过程记录。
