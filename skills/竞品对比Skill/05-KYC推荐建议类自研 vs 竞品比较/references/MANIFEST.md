# 参考文件索引

本文件是 KYC 推荐建议类自研 vs 竞品比较评测协议的导航地图。

- **绝对评分层**：rubric、golden cases、root cause、tool list 提供单模型绝对评分标准，继承第五类 KYC 推荐建议 self_judge 的维度、封顶和根因体系。
- **compare 专属层**：comparison protocol 与 whole-chain comparison 负责定义同题比较和整体链路差异解释。

## compare 专属参考

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [comparison_protocol.md](comparison_protocol.md) | 定义 pairwise 比较流程、先绝对后相对、我方优劣/竞品优点/shared failures 判定规则 | 步骤 4 比较前必读 |
| [whole_chain_comparison.md](whole_chain_comparison.md) | 说明真实输入结构、答案锚点、KYC/context 读取、`chain[*].tools[*]` 读取路径和整体链路差异解释方法 | 步骤 2 链路诊断前必读 |

## 评分细则（rubric/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](rubric/_index.md) | 维度池、动态权重、运行时新增维度规则、KYC 强度判断和封顶索引 | 步骤 0 分析题目前通读 |
| [raw-score-scale.md](rubric/raw-score-scale.md) | 六档原始分量表 | 评分前必读 |
| [intent_profile_understanding.md](rubric/intent_profile_understanding.md) | 意图与画像理解 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [scenario_emotion_recognition.md](rubric/scenario_emotion_recognition.md) | 场景与情绪识别 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [suitability_personalization.md](rubric/suitability_personalization.md) | 适当性与个性化 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [evidence_integration.md](rubric/evidence_integration.md) | 多维证据整合 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [decision_actionability.md](rubric/decision_actionability.md) | 决策可执行性 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [risk_boundary_control.md](rubric/risk_boundary_control.md) | 风险控制与边界 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [product_universe_fit.md](rubric/product_universe_fit.md) | 产品池与配置角色适配 | ETF/基金/资产组合/股票池推荐、核心-卫星配置等场景 |
| [recommendation_stability.md](rubric/recommendation_stability.md) | 推荐稳定性与变化解释 | 历史对话、多次同类推荐、线上稳定性信号等场景 |
| [composition_credibility.md](rubric/composition_credibility.md) | 表达可信度 | 步骤 0 判断适用性 + 步骤 1 评分 |
| [tool_usage.md](rubric/tool_usage.md) | 工具使用合理性 | 步骤 2 评分 |
| [cap_missing_kyc_profile.md](rubric/cap_missing_kyc_profile.md) | 封顶：未使用 KYC 画像 | 步骤 3 |
| [cap_misread_emotional_loss_context.md](rubric/cap_misread_emotional_loss_context.md) | 封顶：误读亏损/情绪场景 | 步骤 3 |
| [cap_fabricated_user_profile.md](rubric/cap_fabricated_user_profile.md) | 封顶：虚构用户画像 | 步骤 3 |
| [cap_missing_action_for_decision_request.md](rubric/cap_missing_action_for_decision_request.md) | 封顶：决策请求无操作建议 | 步骤 3 |
| [cap_missing_required_evidence.md](rubric/cap_missing_required_evidence.md) | 封顶：遗漏必要证据 | 步骤 3 |
| [cap_overconfident_or_unsuitable_recommendation.md](rubric/cap_overconfident_or_unsuitable_recommendation.md) | 封顶：过度确定/不合适推荐 | 步骤 3 |
| [cap_template_generic_advice.md](rubric/cap_template_generic_advice.md) | 封顶：模板化通用建议 | 步骤 3 |

## 专家案例基准（golden_cases/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](golden_cases/_index.md) | 13 个专家案例基准和 hard checks | 步骤 0 分析题目时读取，用于命中检测 |
| [image_annotation_anchors.md](golden_cases/image_annotation_anchors.md) | docx 截图红绿批注沉淀的私人投顾感、产品池、稳定性、情绪场景和可执行动作 hard checks | 步骤 0 与 `_index.md` 一并读取 |

## 根因归因体系（root-cause/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](root-cause/_index.md) | L1 阶段、证据规则、置信度规则、选择规则 | 步骤 2 诊断前通读 |
| [intent.md](root-cause/intent.md) | L1: intent — 推荐任务和决策类型理解 | 步骤 2 |
| [context.md](root-cause/context.md) | L1: context — KYC/历史上下文/持仓/偏好使用 | 步骤 2 |
| [evidence.md](root-cause/evidence.md) | L1: evidence — 推荐证据支撑 | 步骤 2 |
| [tool.md](root-cause/tool.md) | L1: tool — 工具选择与执行 | 步骤 2 |
| [reasoning.md](root-cause/reasoning.md) | L1: reasoning — 推荐推理、适当性、仓位和触发条件 | 步骤 2 |
| [composition.md](root-cause/composition.md) | L1: composition — 答案组织和表达可信度 | 步骤 2 |
| [safety_or_compliance.md](root-cause/safety_or_compliance.md) | L1: safety_or_compliance — 过度确定、风险边界和不适当推荐 | 步骤 2 |

## 工具列表（tool_list/）

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [_index.md](tool_list/_index.md) | 完整工具总览列表（名称 + 功能描述） | 步骤 2 评分 tool_usage 前必读 |
| [search.md](tool_list/search.md) | Search 搜索工具用法规则 | 按需 |
| [finquery.md](tool_list/finquery.md) | FinQuery 金融查询工具用法规则 | 按需 |
| [backtest.md](tool_list/backtest.md) | BackTest 回测工具用法规则 | 按需 |
| [forecast.md](tool_list/forecast.md) | Forecast 预测工具用法规则 | 按需 |
| [accessingfulltext.md](tool_list/accessingfulltext.md) | AccessingFullText 全文阅读工具规则 | 按需 |
| [searchimage.md](tool_list/searchimage.md) | SearchImage 图片搜索工具规则 | 按需 |
| [customerservicefaq.md](tool_list/customerservicefaq.md) | CustomerServiceFAQ 客服 FAQ 工具规则 | 按需 |
| [saveuserprofile.md](tool_list/saveuserprofile.md) | SaveUserProfile 用户画像工具规则 | 按需 |
| [codeinterpreter.md](tool_list/codeinterpreter.md) | CodeInterpreter 工具规则 | 按需 |

## 输出契约

| 文件 | 用途 | 何时读取 |
|---|---|---|
| [output-schema_round1_zh.md](output-schema_round1_zh.md) | Round 1：同题校验、共享权重、KYC 强度识别、两边证据摘要 | 步骤 0 后 |
| [output-schema_zh.md](output-schema_zh.md) | Pairwise JSON 输出契约、双边证据对象和比较结论格式 | 步骤 5 序列化时 |

## 关键依赖

- 步骤 0 题目分析 -> 依赖 `rubric/_index.md`（维度池 + 运行时新增维度 + KYC 强度指南）+ `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` + `output-schema_round1_zh.md`
- `tool_usage` 维度评分 -> 依赖 `whole_chain_comparison.md` + `tool_list/_index.md` + 各工具详细规则；真实工具调用从 `chain[*].tools[*]` 读取
- 根因 L2 的典型受影响维度 -> 反向映射到 rubric 各维度文件
- 封顶规则触发 -> 影响根因选择规则（`root-cause/_index.md` 选择规则）

## 协议步骤到文件的映射

| 协议步骤 | 操作 | 读取文件 |
|---|---|---|
| 步骤 0：分析题目 | 同题校验 + KYC 强度识别 + 适用性判断 + 动态权重 + 临时维度 + 案例命中 | `rubric/_index.md` + `golden_cases/_index.md` + `golden_cases/image_annotation_anchors.md` + `output-schema_round1_zh.md` |
| 步骤 1：分别做绝对评分 | 逐维度评分（仅活跃维度） | `rubric/_index.md` + 各维度文件 + `rubric/raw-score-scale.md` |
| 步骤 2：诊断整体链路 | tool_usage 评分 + KYC/context 使用检查 + 整体链路差异解释 + 根因选择 | `whole_chain_comparison.md` + `rubric/tool_usage.md` + `tool_list/_index.md` + 相关工具文件 + `root-cause/_index.md` + 对应 L1 文件 |
| 步骤 3：应用封顶规则 | 双边分别检查 cap，使用同一 hard checks | `rubric/_index.md` + 对应 `rubric/cap_*.md` 文件 |
| 步骤 4：逐维比较 | 先绝对后相对，输出我方优势/弱点、竞品优点、shared failures | `comparison_protocol.md` |
| 步骤 5：序列化输出 | 双边绝对评分 + 逐维比较 + 自然语言 | `output-schema_zh.md` |
