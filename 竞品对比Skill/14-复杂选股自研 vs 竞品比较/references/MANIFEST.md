# 参考文件索引

本文件是复杂选股自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供第 14 类复杂选股单模型绝对评分标准。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、自研优劣/竞品优点/shared failures 判定规则 | 步骤 4 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则索引 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分制定义（0/20/40/60/80/100） | 评分前必读 |
| [intent_condition_extraction.md](rubric/intent_condition_extraction.md) | 意图与条件抽取维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [financial_semantics_and_caliber.md](rubric/financial_semantics_and_caliber.md) | 金融语义与口径维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [screening_plan_decomposition.md](rubric/screening_plan_decomposition.md) | 筛选规划拆解维度 | 步骤 0 判断适用性 + 步骤 1/2 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具与信源匹配维度 | 步骤 2 链路诊断时评分 |
| [result_correctness_and_coverage.md](rubric/result_correctness_and_coverage.md) | 结果正确性与覆盖维度 | 步骤 1 评分 |
| [ranking_and_decision_actionability.md](rubric/ranking_and_decision_actionability.md) | 排序与决策可执行性维度 | 步骤 1 评分 |
| [data_logic_time_boundary.md](rubric/data_logic_time_boundary.md) | 数据逻辑与时间边界维度 | 步骤 1/2 评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度维度 | 步骤 1 评分 |

## 封顶规则（rubric/cap_*.md）

| 文件 | 何时读取 |
|---|---|
| [cap_core_condition_omitted_or_rewritten.md](rubric/cap_core_condition_omitted_or_rewritten.md) | 核心筛选条件被遗漏或改写时 |
| [cap_hard_financial_semantics_or_caliber_error.md](rubric/cap_hard_financial_semantics_or_caliber_error.md) | 金融语义、指标公式、业务口径硬错时 |
| [cap_unsupported_data_forced_output.md](rubric/cap_unsupported_data_forced_output.md) | 数据不可得、已停更或工具不支持却强行输出时 |
| [cap_wrong_tool_strategy.md](rubric/cap_wrong_tool_strategy.md) | 工具策略与结构化/非标信息需求明显不匹配时 |
| [cap_layered_or_temporal_screening_failure.md](rubric/cap_layered_or_temporal_screening_failure.md) | 分层、跨领域交集或先后时序筛选失败时 |
| [cap_missing_required_ranking_or_fields.md](rubric/cap_missing_required_ranking_or_fields.md) | 用户要求排序、Top N、选一只或指定字段但未满足时 |
| [cap_unverifiable_result_or_data_hallucination.md](rubric/cap_unverifiable_result_or_data_hallucination.md) | 候选股、数值、公式或事实无法验证或与工具结果冲突时 |
| [cap_chart_or_table_without_decision_value.md](rubric/cap_chart_or_table_without_decision_value.md) | 大量图表/表格没有帮助决策时 |

## 根因归因（root-cause/）

| 文件 | 用途 |
|---|---|
| [_index.md](root-cause/_index.md) | 根因归因体系总览 |
| [intent.md](root-cause/intent.md) | 长问句条件、否定条件、隐性指令、输出要求遗漏 |
| [semantics.md](root-cause/semantics.md) | 金融指标、交易语义、业务口径、数据频率误解 |
| [planning.md](root-cause/planning.md) | 未分层筛选、前后关系丢失、跨领域交集未处理 |
| [tool.md](root-cause/tool.md) | 工具选择、关键词、参数、交叉验证或读取输出错误 |
| [data_logic.md](root-cause/data_logic.md) | 日期、交易日、分时、公式、不可用数据边界错误 |
| [result.md](root-cause/result.md) | 候选池、排序、字段、无结果说明不满足要求 |
| [composition.md](root-cause/composition.md) | 表达混乱、数据堆砌、表格图表无决策价值 |

## 其他参考

| 文件 | 用途 |
|---|---|
| [tool_list/_index.md](tool_list/_index.md) | 复杂选股常用工具与信源匹配 |
| [golden_cases/_index.md](golden_cases/_index.md) | 40 个专家案例 hard checks |
| [golden_cases/image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 图片批注与截图中沉淀的专家知识 |
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、双边证据摘要、比较焦点 |
| [output-schema_zh.md](output-schema_zh.md) | Round 2：Pairwise JSON 输出契约、双边证据对象和比较结论格式 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md`
- `tool_usage` 维度评分 → 依赖 `whole_chain_comparison.md` + `tool_list/_index.md`；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 选择 → 依赖 `root-cause/_index.md` 和对应 L1 文件
- 封顶规则触发 → 依赖对应 `rubric/cap_*.md`
- Pairwise 比较 → 依赖 `comparison_protocol.md` 和 `output-schema_zh.md`

## 协议步骤映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：建立共享框架 | 条件抽取 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度） | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` |
| 步骤 2：诊断整体链路 | `tool_usage` 评分 + 链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + `root-cause/_index.md` |
| 步骤 3：应用封顶规则 | 分别检查两边封顶触发 | 对应 `rubric/cap_*.md` 文件 |
| 步骤 4：逐维比较 | 先绝对后相对，输出自研优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 5：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
