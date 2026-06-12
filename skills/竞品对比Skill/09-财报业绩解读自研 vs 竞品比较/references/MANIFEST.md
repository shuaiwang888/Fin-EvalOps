# 参考文件索引

本文件是财报业绩解读自研 vs 竞品比较评测协议的导航地图。

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
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 + 动态加权公式 | 评分前必读 |
| [intent_understanding.md](rubric/intent_understanding.md) | 意图理解与任务完成维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [report_data_accuracy.md](rubric/report_data_accuracy.md) | 财报数据与口径准确性维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [primary_evidence_quality.md](rubric/primary_evidence_quality.md) | 公告全文与证据质量维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [causal_attribution_depth.md](rubric/causal_attribution_depth.md) | 归因深度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [business_financial_linkage.md](rubric/business_financial_linkage.md) | 业务财务联动维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [forward_investment_judgment.md](rubric/forward_investment_judgment.md) | 前瞻与投资判断维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度维度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性维度 | 步骤 0 判断适用性 + 步骤 2 评分 |
| [cap_hard_fact_or_caliber_error.md](rubric/cap_hard_fact_or_caliber_error.md) | 封顶规则：硬性事实或口径错误（上限 40） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |
| [cap_missing_primary_disclosure.md](rubric/cap_missing_primary_disclosure.md) | 封顶规则：遗漏关键原始披露（上限 55） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |
| [cap_wrong_special_event_explanation.md](rubric/cap_wrong_special_event_explanation.md) | 封顶规则：特殊事件解释错误（上限 45） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |
| [cap_surface_financial_formula_only.md](rubric/cap_surface_financial_formula_only.md) | 封顶规则：只做表层财务公式解释（上限 60） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |
| [cap_unverifiable_or_hallucinated_numbers.md](rubric/cap_unverifiable_or_hallucinated_numbers.md) | 封顶规则：不可验证或幻觉数字（上限 50） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |
| [cap_missing_required_conclusion.md](rubric/cap_missing_required_conclusion.md) | 封顶规则：缺少必要结论（上限 65） | 步骤 1 绝对评分或步骤 2 链路诊断后检查 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 30 个专家案例 hard checks + 跨案例判分锚点 | 步骤 0 分析题目时读取，用于命中检测 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | 链路阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 理解问题（5 个 L2） | 步骤 2 归因时 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 检索信息（6 个 L2） | 步骤 2 归因时 |
| [tool.md](root-cause/tool.md) | L1: tool — 选择与执行工具（7 个 L2） | 步骤 2 归因时 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 财务与业务推理（8 个 L2） | 步骤 2 归因时 |
| [composition.md](root-cause/composition.md) | L1: composition — 组织答案（5 个 L2） | 步骤 2 归因时 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述） | 步骤 2 评分 `tool_usage` 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文阅读工具用法规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 计算工具用法规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 4 序列化时 |

## 关键依赖

- 步骤 0 题目分析 → 依赖 `rubric/_index.md`（维度列表 + 适用性指南）+ 各维度文件（`## 适用性判断`）+ `golden_cases/_index.md`
- `tool_usage` 维度评分 → 依赖 `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的“典型受影响维度”列 → 反向映射到 rubric 各维度文件
- 封顶规则触发 → 影响根因选择和最终比较结论，但不替代维度评分

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 同题校验 + 适用性判断 + 动态权重 + 案例命中 | `rubric/_index.md` + 各维度文件 `## 适用性判断` + `golden_cases/_index.md` + `output-schema_round1_zh.md` |
| 步骤 1：分别做绝对评分 | 对自研和竞品逐维评分（仅活跃维度）+ 封顶检查 | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 2：诊断整体链路 | `tool_usage` 评分 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 4：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
