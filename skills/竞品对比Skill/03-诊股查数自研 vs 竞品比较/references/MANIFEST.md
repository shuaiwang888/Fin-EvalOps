# 参考文件索引

本文件是自研 vs 竞品比较评测协议的导航地图。

- **原 03 继承层**：rubric、golden cases、root cause、tool list 继续提供单模型绝对评分标准。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 3 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表 + 动态权重分配规则 + 封顶规则注意事项 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表（0/20/40/60/80/100） | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度 | 步骤 0 + 步骤 1 |
| [data_accuracy_coverage.md](rubric/data_accuracy_coverage.md) | 数据准确性与覆盖 | 步骤 0 + 步骤 1 |
| [time_caliber_precision.md](rubric/time_caliber_precision.md) | 时间、口径与粒度 | 步骤 0 + 步骤 1 |
| [calculation_comparison.md](rubric/calculation_comparison.md) | 计算与对比 | 步骤 0 + 步骤 1 |
| [analysis_framework_fit.md](rubric/analysis_framework_fit.md) | 市场分析框架匹配度 | 步骤 0 + 步骤 1 |
| [insight_extension.md](rubric/insight_extension.md) | 延伸洞察与增量信息 | 步骤 0 + 步骤 1 |
| [result_verifiability.md](rubric/result_verifiability.md) | 结果可验证性 | 步骤 0 + 步骤 1 |
| [presentation_visualization.md](rubric/presentation_visualization.md) | 呈现与可视化 | 步骤 0 + 步骤 1 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性 | 步骤 2 |
| [cap_hard_data_or_fact_error.md](rubric/cap_hard_data_or_fact_error.md) | 封顶：硬性数据/事实错误（上限 35） | 步骤 3 |
| [cap_missing_required_data.md](rubric/cap_missing_required_data.md) | 封顶：必要数据缺失（上限 60） | 步骤 3 |
| [cap_time_or_caliber_error.md](rubric/cap_time_or_caliber_error.md) | 封顶：时间/口径错误（上限 45） | 步骤 3 |
| [cap_intraday_precision_missing.md](rubric/cap_intraday_precision_missing.md) | 封顶：日内精度缺失（上限 55） | 步骤 3 |
| [cap_wrong_analysis_framework.md](rubric/cap_wrong_analysis_framework.md) | 封顶：分析框架错误（上限 55） | 步骤 3 |
| [cap_data_dump_without_insight.md](rubric/cap_data_dump_without_insight.md) | 封顶：数据堆砌无洞察（上限 65） | 步骤 3 |
| [cap_unverifiable_or_fabricated_result.md](rubric/cap_unverifiable_or_fabricated_result.md) | 封顶：不可验证或疑似编造（上限 50） | 步骤 3 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 21 个专家案例 hard checks + 跨案例判分锚点 | 步骤 0 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片/截图沉淀的补充锚点：可视化、表格、工具失败类型、截图式好坏答案特征 | 题目涉及图表、截图、多周期展示、工具错误归因时读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 理解问题 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 检索数据/证据 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 选择与执行工具 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 计算、口径和金融推理 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 组织答案 | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述） | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 计算与表格处理工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文读取工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md`（维度列表 + 适用性指南）+ `golden_cases/_index.md` + 按需 `golden_cases/image_annotation_anchors.md`
- `tool_usage` 维度评分 → 依赖 `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 专家案例命中 → 依赖 `golden_cases/_index.md` 的 hard checks 和跨案例判分锚点
- 根因 L2 的“典型受影响维度”列 → 反向映射到 rubric 各维度文件
- 封顶规则触发 → 影响根因选择规则（`_index.md` 选择规则第 2 步）

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + `golden_cases/_index.md` + 按需 `image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 专家案例核验 + 逐维度评分（仅活跃维度，tool_usage 除外）+ 封顶检查 | `golden_cases/_index.md` + 活跃维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
