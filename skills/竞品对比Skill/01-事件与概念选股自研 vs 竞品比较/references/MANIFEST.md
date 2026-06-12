# 参考文件索引

本文件是自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供单模型绝对评分标准。
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
| [raw-score-scale.md](rubric/raw-score-scale.md) | 0-5 分制定义 + 动态加权公式 | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [event_abstraction.md](rubric/event_abstraction.md) | 事件抽象度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [industry_mapping.md](rubric/industry_mapping.md) | 产业链映射维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [ranking_judgment.md](rubric/ranking_judgment.md) | 排序判断维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [logic_closure.md](rubric/logic_closure.md) | 逻辑闭环维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [timeliness_fact_boundary.md](rubric/timeliness_fact_boundary.md) | 时效性与事实边界维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [credibility_expression.md](rubric/credibility_expression.md) | 可信度与表达维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [cap_hard_time_or_fact_error.md](rubric/cap_hard_time_or_fact_error.md) | 封顶规则：硬性时间或事实错误（上限 40） | 步骤 3 封顶时 |
| [cap_missing_required_ranking.md](rubric/cap_missing_required_ranking.md) | 封顶规则：遗漏必要排序（上限 60） | 步骤 3 封顶时 |
| [cap_data_dump_without_core_rationale.md](rubric/cap_data_dump_without_core_rationale.md) | 封顶规则：数据堆砌无核心论证（上限 55） | 步骤 3 封顶时 |
| [cap_wrong_evidence_type.md](rubric/cap_wrong_evidence_type.md) | 封顶规则：证据类型错误（上限 50） | 步骤 3 封顶时 |
| [cap_unverifiable_subjective_expression.md](rubric/cap_unverifiable_subjective_expression.md) | 封顶规则：不可验证的主观表达（上限 65） | 步骤 3 封顶时 |
| [cap_forced_mapping_or_entity_boundary_error.md](rubric/cap_forced_mapping_or_entity_boundary_error.md) | 封顶规则：强行映射或实体边界错误（上限 50） | 步骤 3 封顶时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 40 个专家案例 hard checks + 跨案例判分锚点 | 步骤 0 分析题目时读取，用于命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片人工批注补充锚点：图表、排序、交易性价比、非标产业证据、实体边界和追加场景 hard checks | 步骤 0 与 `_index.md` 一并读取；命中特高压+柔直、两会、溴素、铜、SOFC、美股机器人等场景时重点使用 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 理解问题（4 个 L2） | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 检索信息（6 个 L2） | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 选择与执行工具（5 个 L2） | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 推导投资逻辑（8 个 L2） | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 组织答案（5 个 L2） | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述） | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md`（维度列表 + 适用性指南）+ 各维度文件（`## 适用性判断`）+ `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md`
- `tool_usage` 维度评分 → 依赖 `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的"典型受影响维度"列 → 反向映射到 rubric 各维度文件
- 封顶规则触发 → 影响根因选择规则（`_index.md` 选择规则第 2 步）

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
