# 参考文件索引

本文件是复合意图类问题自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供单模型绝对评分标准。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。
- **第 6 类维度体系保持不变**：比较层不得新增、删除或重命名 `06-compound-intent` 的既有评测维度、封顶规则和根因体系。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 3 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则注意事项 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 + 动态加权公式 | 评分前必读 |
| [intent_decomposition.md](rubric/intent_decomposition.md) | 意图拆解维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [task_coverage_priority.md](rubric/task_coverage_priority.md) | 子任务覆盖与主次维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [multi_source_evidence_integration.md](rubric/multi_source_evidence_integration.md) | 多源证据整合维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [analysis_chain_closure.md](rubric/analysis_chain_closure.md) | 分析链路闭环维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [data_logic_rigor.md](rubric/data_logic_rigor.md) | 数据与逻辑严谨性维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [decision_actionability.md](rubric/decision_actionability.md) | 决策表达与可执行性维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [composition_readability.md](rubric/composition_readability.md) | 结构与可读性维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |

## 封顶规则

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [cap_missed_major_subtask.md](rubric/cap_missed_major_subtask.md) | 封顶规则：遗漏主要子任务（上限 65） | 步骤 1 绝对评分封顶检查 |
| [cap_data_or_case_unreliable.md](rubric/cap_data_or_case_unreliable.md) | 封顶规则：数据或案例不可靠（上限 55） | 步骤 1 绝对评分封顶检查 |
| [cap_calculation_or_time_window_error.md](rubric/cap_calculation_or_time_window_error.md) | 封顶规则：计算或时间窗口错误（上限 55） | 步骤 1 绝对评分封顶检查 |
| [cap_information_pile_without_synthesis.md](rubric/cap_information_pile_without_synthesis.md) | 封顶规则：信息堆砌无综合（上限 60） | 步骤 1 绝对评分封顶检查 |
| [cap_missing_required_decision_output.md](rubric/cap_missing_required_decision_output.md) | 封顶规则：遗漏必要决策输出（上限 65） | 步骤 1 绝对评分封顶检查 |
| [cap_wrong_or_shallow_evidence_mix.md](rubric/cap_wrong_or_shallow_evidence_mix.md) | 封顶规则：证据组合错误或浅层（上限 60） | 步骤 1 绝对评分封顶检查 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 10 个专家案例基准和 hard checks | 步骤 0 分析题目时读取，用于命中检测 |
| [image_output_anchors.md](golden_cases/image_output_anchors.md) | 从问财/豆包截图和人工批注提取的好答案、差答案、封顶和归因锚点 | 步骤 0 与 `_index.md` 一并读取；输入包含截图 OCR、人工批注或同类场景时重点使用 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 意图拆解 | 步骤 2 归因时 |
| [coverage.md](root-cause/coverage.md) | L1: coverage — 子任务覆盖 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 证据整合 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 工具编排 | 步骤 2 归因时 |
| [data_logic.md](root-cause/data_logic.md) | L1: data_logic — 数据逻辑 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 推理闭环 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 答案组织 | 步骤 2 归因时 |

## 工具列表（tool_list/）

工具列表直接复用事件概念选股 skill 的工具定义，已复制到当前目录：

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述） | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文读取工具用法规则 | 按需 |
| [searchimage.md](tool_list/searchimage.md) | SearchImage 图片搜索工具用法规则 | 按需 |
| [customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 客服知识工具用法规则 | 按需 |
| [saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 用户画像保存工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 计算与分析工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md`（维度列表 + 适用性指南）+ 各维度文件 + `golden_cases/_index.md` + `golden_cases/image_output_anchors.md`
- `tool_usage` 维度评分 → 依赖 `whole_chain_comparison.md` + `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的“典型受影响维度”列 → 反向映射到 rubric 各维度文件
- 封顶规则触发 → 影响根因选择规则（`_index.md` 选择规则第 2 步）

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 同题校验 + 适用性判断 + 共享动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 + `golden_cases/_index.md` + `golden_cases/image_output_anchors.md` + `output-schema_round1_zh.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
