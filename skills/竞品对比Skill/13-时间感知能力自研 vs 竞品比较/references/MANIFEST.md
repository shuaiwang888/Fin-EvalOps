# 参考文件索引

本文件是时间感知能力自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 沿用第 13 类时间感知能力的单模型评分标准。
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
| [temporal_intent_recognition.md](rubric/temporal_intent_recognition.md) | 时间意图识别维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [anchor_date_resolution.md](rubric/anchor_date_resolution.md) | 锚定日期解析维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [market_calendar_status.md](rubric/market_calendar_status.md) | 市场交易日历状态维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [data_asof_freshness.md](rubric/data_asof_freshness.md) | 数据时点与新鲜度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [period_disclosure_mapping.md](rubric/period_disclosure_mapping.md) | 报告期与披露期映射维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [premise_correction_clarification.md](rubric/premise_correction_clarification.md) | 时间前提纠错与澄清维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [answer_composition_credibility.md](rubric/answer_composition_credibility.md) | 答案组织与可信边界维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [cap_hard_wrong_anchor_date.md](rubric/cap_hard_wrong_anchor_date.md) | 封顶规则：核心日期锚点错误 | 封顶检查时 |
| [cap_market_closed_answered_as_open.md](rubric/cap_market_closed_answered_as_open.md) | 封顶规则：休市日按开盘回答 | 封顶检查时 |
| [cap_stale_data_masquerading_as_today.md](rubric/cap_stale_data_masquerading_as_today.md) | 封顶规则：旧数据冒充今天/最新 | 封顶检查时 |
| [cap_missing_required_premise_correction.md](rubric/cap_missing_required_premise_correction.md) | 封顶规则：缺失必要前提纠错 | 封顶检查时 |
| [cap_fiscal_period_disclosure_error.md](rubric/cap_fiscal_period_disclosure_error.md) | 封顶规则：财报/分红/报告期映射错误 | 封顶检查时 |
| [cap_fabricated_time_fact.md](rubric/cap_fabricated_time_fact.md) | 封顶规则：编造时间事实 | 封顶检查时 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | docx 正文沉淀的时间感知 hard checks 和跨案例锚点 | 步骤 0 命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 图片截图中的补充专家知识：休市、旧数据、财报披露期、去年/年中映射 | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | L1/L2 根因、证据规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 时间意图和锚点理解 | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 时间证据、日历和 as-of 检索 | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 时间核验工具策略 | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 自然日/交易日/报告期推理 | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 最终答案中的时间边界呈现 | 步骤 2 归因时 |
| [capability_gap.md](root-cause/capability_gap.md) | L1: capability_gap — 数据覆盖或工具能力限制 | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 时间感知题常见工具用途和错误模式 | 步骤 2 评分 `tool_usage` 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文读取工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 日期计算和批量核验规则 | 按需 |
| [searchimage.md](tool_list/searchimage.md) | SearchImage 截图/图表时间锚点识别规则 | 按需 |
| [customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 在时间感知评测中的非主工具边界 | 按需 |
| [saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 在时间感知评测中的非主工具边界 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享时间锚点、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 时间锚点抽取 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | tool_usage 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
