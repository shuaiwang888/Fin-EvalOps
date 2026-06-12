---
name: kyc-recommendation-suggestions-self-vs-competitor
description: 用于比较同一 case_id 下自研模型与一个竞品模型在 KYC 推荐建议类金融问题上的最终答案和完整链路质量。适用于标的推荐、基金/ETF 推荐、买卖持仓建议、资产配置、解套加仓减仓、结合用户风险目标的投顾式决策支持，输入包括两边用户 query、context、meta.user_investment_goal、plan、工具调用输入输出和最终回答，输出自研 vs 竞品比较 JSON 评测结果。
---

# KYC 推荐建议类自研 vs 竞品比较评测协议

本协议用于比较**同一 `case_id`（同题配对键）下**自研模型与一个竞品模型在 KYC 推荐建议类金融问题上的**整体链路 + 最终回答**。它定义了 KYC 推荐建议类问题的绝对评分体系（由 rubric、golden cases、root cause 构成），以及 pairwise 比较协议与链路差异解释方法。

## 协议边界

- **绝对评分**：判断单个模型在 KYC 推荐建议任务上答得好不好。
- **横向比较**：
  1. 对同题两边分别做绝对评分；
  2. 再比较自研强项、自研弱项和竞品强项；
  3. 最后用两边完整链路解释这些答案差异是怎么产生的。
- 比较对象不是“两个最终答案”这么窄，而是：
  - 同一用户问题；
  - 两边上下文、历史提问和可见 KYC/画像/持仓/风险偏好信息；
  - 两边最终回答；
  - 两边可见整体链路，包括 `chain[*].plan`、`chain[*].tools[*]`、工具输入和工具输出；
  - 两边 `meta.user_investment_goal`（若存在）。
- 链路的价值在于解释答案差异，不是脱离答案单独评判“工程美学”。

## 适用范围

仅在以下条件同时满足时使用本协议：
- 题目属于 KYC 推荐建议类金融任务，包括：
  - 推荐适合我的股票、基金、ETF、行业、资产或组合；
  - 能不能买、是否继续持有、该割肉还是加仓、怎么控制仓位；
  - 结合我的目标、风险、资金、持仓、风格给建议；
  - 宏观/行业/市场情景下的方向选择、资产比较和配置顺序；
  - 用户处于浮亏、套牢、迷茫、信心受挫等真实投资处境时的投顾式建议。
- 输入中存在同一 `case_id` 对应的两份记录；
- 两份记录分别代表自研模型与**一个**竞品模型；
- 当前任务目标是回答：
  - 自研模型相比竞品好在哪里；
  - 自研模型相比竞品差在哪里；
  - 竞品模型哪里值得学习。

不适用于：
- 普通单模型质检；
- 不同问题之间的横向比较；
- 一次同时比较多个竞品模型；
- 纯行情查询、纯事实查询、客服问题、图片搜索或不需要用户适配的普通资料总结；
- 只看最终答案、完全不需要链路归因的轻量 benchmark。

若问题同时包含分析和推荐，以是否需要给用户做适配后的决策建议为准。KYC 推荐建议适用问题默认采用强 KYC 标准：只要答案会形成个人投资建议，就应检查模型是否主动获取并使用用户 KYC 数据。

## 输入语义

每次评测至少读取：
- `case_id`：同题配对键（自研与竞品共享）；
- 用户问题；
- 自研模型完整记录；
- 竞品模型完整记录。

### 最终答案锚点

- 自研模型：优先使用 `text_answer` 作为最终答案主锚点；
- 竞品模型：若 `text_answer` 为空，则使用 `answer` 作为最终答案主锚点；
- 若编排层已提前生成统一字段，可直接读取归一化后的最终答案，但不得因此改变原始证据指针。

### KYC 与链路结构

- `meta.user_investment_goal`（若存在）是评测员判断模型是否主动使用 KYC 数据、推荐是否针对该用户适配的关键参考；
- `context` 中的历史提问、历史持仓、画像、风险偏好、成本、期限、亏损状态或用户自述，也是 KYC 推荐建议类问题的重要输入；
- KYC 数据可以来自用户画像工具、用户画像存储、历史 `context`、当前问题中的自述信息或链路中可见的画像检索结果；
- 不要把“context 中没有 KYC”作为放过模型的理由；关键是模型面对推荐/交易/配置问题时是否遵循“先取 KYC、再做推荐”的标准；
- `tool_usage` 是**评测维度名**，不是输入 JSON 的字段名；
- 真实工具调用从 `chain[N].tools[M]` 读取；
- 顶层 `tools` 字段即便存在，也可能为空，不能把它当成主要链路来源；
- 自研记录通常是多步 `chain`，`plan` 较完整；
- 竞品记录可能只有一个 `chain` step，`plan` 为空，但 `chain[0].tools` 仍包含可用的工具调用证据。

详细规则见：
- [references/comparison_protocol.md](references/comparison_protocol.md)
- [references/whole_chain_comparison.md](references/whole_chain_comparison.md)

## 执行协议

0. **先分析题目，建立共享评测框架**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、[references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)。
   仅根据 `question`、必要 `context`、可见 `meta.user_investment_goal` 和已提供的 `online_dimension_signals` 判断本题推荐目标、KYC 强度、证据需求、决策强度、产品池要求、稳定性要求和风险责任。
   同一题下，自研与竞品必须使用**同一套**适用性、运行时新增维度和权重，避免把权重差异误当成模型差异。
   对 KYC 推荐建议维度判断适用性：
   - `relevant`：本题核心判断依据；
   - `supplementary`：有参考价值但不是主矛盾；
   - `not_applicable`：该维度与题目无关，跳过评分。
   动态权重总和必须为 100，并记录到输出的 `weight_assignment`。若线上数据暴露的关键缺口无法被现有维度清楚覆盖，可按 KYC 推荐建议原协议新增临时评分维度，并直接并入 `weight_assignment` 与双方 `dimension_scores`。
   对 KYC 推荐建议适用问题，KYC 强度至少为 relevant：即使问题只写“推荐一下”“该不该买”“怎么配置”，只要答案会形成个人投资建议，就应评估模型是否主动使用用户 KYC 数据。
   命中专家案例或同类语义时，必须使用对应 hard checks。

1. **先分别做绝对评分**
   对自研与竞品分别按本 skill 定义的 KYC 推荐建议维度评分，种子维度包括：
   - `intent_profile_understanding`
   - `scenario_emotion_recognition`
   - `suitability_personalization`
   - `evidence_integration`
   - `decision_actionability`
   - `risk_boundary_control`
   - `product_universe_fit`
   - `recommendation_stability`
   - `composition_credibility`（supplementary）
   - `tool_usage`

   若步骤 0 新增临时评分维度，也必须对双方使用同一新增维度评分。
   除 `tool_usage` 外，先只依据用户问题、必要上下文、可见 KYC 信息和各自最终答案评分；不得因为另一方更差，就抬高本方绝对分。每个活跃维度的 `raw_score` 必须取六档值：0/20/40/60/80/100。
   必须判断最终答案是否体现用户 KYC 数据对推荐结论的约束，例如风险承受能力、投资期限、资金目标、持仓背景、交易经验、偏好或历史亏损处境。若提供了 `meta.user_investment_goal`，必须将答案与该画像对照。

2. **再分别诊断两边整体链路**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)、[references/tool_list/_index.md](references/tool_list/_index.md) 和 [references/whole_chain_comparison.md](references/whole_chain_comparison.md)。
   对两边分别检查：
   - 是否正确识别推荐目标、决策类型、用户真实处境和必要上下文；
   - 是否主动读取、调用、检索或引用用户 KYC 数据；
   - 工具选择是否正确；
   - 查询输入是否贴合标的、产品池、风险目标、时间窗口、证据类型和用户处境；
   - 证据是否覆盖市场、宏观、行业、估值、技术、资金、持仓、风险和画像适配维度；
   - 是否有交叉验证；
   - 工具结果是否真正转化成了更好的最终答案。

   当 `plan` 存在时，可结合其判断意图、KYC 画像处理和推理；当 `plan` 为空时，不强行编造“推理文本”归因，优先依据工具行为、证据流和最终答案做判断。
   若链路没有取到可用 KYC，而最终答案又形成推荐或交易建议，应检查答案是否明确说明画像依据不足，并给出分层、条件化、低风险边界清晰的建议或必要追问；否则归因为 `context` / `tool` / `reasoning` 中的 KYC 使用缺失。
   此时评分 `tool_usage`。

3. **应用封顶规则**
   按需读取 [references/rubric/](references/rubric/_index.md) 中的 `cap_*.md` 文件。
   封顶规则限制最终分，不替代维度评分。若多个封顶同时触发，取最低上限。
   自研与竞品必须使用同一套 hard checks；但封顶是否触发分别判断。

4. **最后做 pairwise 比较**
   阅读 [references/comparison_protocol.md](references/comparison_protocol.md)。
   在双方绝对评分完成后，逐维比较：
   - 自研真正做得好的地方；
   - 自研真正落后的地方；
   - 竞品真正值得学习的地方；
   - 双方共同失败点；
   - 哪些链路差异导致了最终答案差异。

   比较时必须坚持：
   - **先绝对、后相对**：双方都差时，先写共同短板，再写谁相对更好；
   - **答案与链路合看**：答案决定质量，链路解释质量是怎么形成的；
   - **证据优先**：每条优势、弱点和学习点都要绑定最终答案、上下文、KYC 信息或链路证据；
   - **不做多模型聚合**：本协议一次只比较一个竞品，跨竞品总结由后续汇总层完成。

5. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 自研与竞品使用同一维度、同一权重、同一 hard checks；
- 不因为相对胜负而改变绝对评分；
- 不因为链路看起来繁复就自动加分；
- 若链路更好但最终答案没有兑现，优点只能记为链路信号，不能替代答案质量；
- 若双方都没有真正完成用户任务，必须明确输出共同不足，不能把“谁稍微好一点”写成高质量答案；
- 最终答案决定用户侧质量，链路只用于归因；
- KYC 推荐建议优先评估是否先理解人和场景，再决定推荐、仓位、期限和风险边界；
- “私人投顾感”是 KYC 推荐建议的重要质量标准：答案要让用户看出模型知道我是谁、我处在什么投资状态、为什么这个建议适合我，而不是只给市场观点或产品榜单；
- 对模板化荐股、窄行业高波动推荐、同类问题推荐不稳定且无解释、过度确定的底部/收益判断、关键数据缺失保持严格扣分；
- 对编造用户画像、忽略亏损/迷茫/套牢情绪、把高风险短线策略推荐给明显不适配的用户保持严格扣分。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
