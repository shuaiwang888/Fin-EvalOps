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
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 评分前必读 |
| [financial_logic_chain.md](rubric/financial_logic_chain.md) | 金融逻辑链维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [market_driver_identification.md](rubric/market_driver_identification.md) | 市场驱动识别维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [evidence_to_conclusion.md](rubric/evidence_to_conclusion.md) | 证据到结论维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [comparison_and_ranking.md](rubric/comparison_and_ranking.md) | 比较与排序维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [scenario_risk_reasoning.md](rubric/scenario_risk_reasoning.md) | 情景与风险推理维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [decision_value_expression.md](rubric/decision_value_expression.md) | 决策价值表达维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [cap_unsupported_prediction_or_recommendation.md](rubric/cap_unsupported_prediction_or_recommendation.md) | 封顶规则：无支撑预测或推荐 | 封顶检查时 |
| [cap_evidence_conclusion_disconnect.md](rubric/cap_evidence_conclusion_disconnect.md) | 封顶规则：结论与证据脱节 | 封顶检查时 |
| [cap_missing_key_market_driver.md](rubric/cap_missing_key_market_driver.md) | 封顶规则：关键市场驱动缺失 | 封顶检查时 |
| [cap_overconfident_risk_commitment.md](rubric/cap_overconfident_risk_commitment.md) | 封顶规则：收益/风险承诺过度 | 封顶检查时 |
| [cap_comparison_logic_error.md](rubric/cap_comparison_logic_error.md) | 封顶规则：比较或排序逻辑错误 | 封顶检查时 |
| [cap_data_dump_without_reasoning.md](rubric/cap_data_dump_without_reasoning.md) | 封顶规则：数据堆砌替代推理 | 封顶检查时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 第 12 类当前未内置具体专家案例；用于记录外部命中案例的读取规则 | 步骤 0 分析题目时读取 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | 图片批注锚点读取规则 | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 理解决策任务 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 证据收集 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 工具策略 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 投资逻辑推导 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 答案组织 | 步骤 2 归因时 |

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

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 决策任务识别 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
