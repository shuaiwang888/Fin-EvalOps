# 参考文件索引

本文件是金融资讯咨询问答自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 沿用第 8 类自研模型 skill 的单模型绝对评分标准。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 3 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度列表、动态权重、封顶规则总览 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档分制定义 | 评分前必读 |
| [intent_fulfillment.md](rubric/intent_fulfillment.md) | 意图满足度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [timeliness_fact_boundary.md](rubric/timeliness_fact_boundary.md) | 时效性与事实边界 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [fact_evidence_quality.md](rubric/fact_evidence_quality.md) | 事实证据质量 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [information_integration.md](rubric/information_integration.md) | 资讯整合与比较 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [investment_mapping.md](rubric/investment_mapping.md) | 投资映射与落地 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [core_signal_extraction.md](rubric/core_signal_extraction.md) | 核心信号提炼 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [nonstandard_source_awareness.md](rubric/nonstandard_source_awareness.md) | 非标准资讯意识 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [credibility_expression.md](rubric/credibility_expression.md) | 可信表达 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [cap_hard_time_or_fact_error.md](rubric/cap_hard_time_or_fact_error.md) | 封顶：硬性时间或事实错误 | 步骤 3 封顶时 |
| [cap_stale_or_wrong_evidence.md](rubric/cap_stale_or_wrong_evidence.md) | 封顶：证据过时或来源类型错误 | 步骤 3 封顶时 |
| [cap_template_answer_without_signal.md](rubric/cap_template_answer_without_signal.md) | 封顶：模板化回答未抓核心信号 | 步骤 3 封顶时 |
| [cap_data_dump_without_judgment.md](rubric/cap_data_dump_without_judgment.md) | 封顶：数据堆砌无判断 | 步骤 3 封顶时 |
| [cap_unverified_rumor_as_fact.md](rubric/cap_unverified_rumor_as_fact.md) | 封顶：传闻当事实 | 步骤 3 封顶时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 21 个专家案例 hard checks 与跨案例锚点 | 步骤 0 分析题目时读取，用于命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片中的市场小段子、调研纪要、大 V/官媒截图补充锚点 | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 根因选择规则、证据规则、置信度规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 意图理解 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 信息证据 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 工具选择与执行 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 推理判断 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 答案组织 | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 工具和来源类型总览 | 步骤 2 评分 `tool_usage` 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文读取工具用法规则 | 按需 |
| [searchimage.md](tool_list/searchimage.md) | SearchImage 图片/截图相关工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 数据处理工具用法规则 | 按需 |
| [customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 客服知识工具用法规则 | 按需 |
| [saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 用户画像保存工具用法规则 | 按需 |

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
- pairwise 比较 → 绝对评分完成后再读取 `comparison_protocol.md`

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | `tool_usage` 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
