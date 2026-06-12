# 分析评价类自研 vs 竞品比较评测协议

本协议用于比较**同一 `case_id`（同题配对键）下**自研模型与一个竞品模型在分析评价类金融问答中的**整体链路 + 最终回答**。它定义了分析评价类问题的绝对评分体系（由 rubric、golden cases、root cause 构成），以及 pairwise 比较协议与链路差异解释方法。

## 协议边界

- **绝对评分**：判断单个模型在分析评价类金融任务上答得好不好。
- **横向比较**：
  1. 对同题两边分别做绝对评分；
  2. 再比较自研强项、自研弱项和竞品强项；
  3. 最后用两边完整链路解释这些答案差异是怎么产生的。
- 比较对象不是“两个最终答案”这么窄，而是：
  - 同一用户问题；
  - 两边上下文和可见用户画像/持仓/风险偏好信息；
  - 两边最终回答；
  - 两边可见整体链路，包括 `chain[*].plan`、`chain[*].tools[*]`、工具输入和工具输出。
- 链路的价值在于解释答案差异，不是脱离答案单独评判“工程美学”。

## 适用范围

仅在以下条件同时满足时使用本协议：
- 题目属于分析评价类金融问答，包括：
  - 股票、指数、基金、ETF、宏观资产的分析、评价、诊断、趋势判断；
  - 为什么上涨、为什么没涨、为什么冲高回落等行情归因；
  - 能不能买、要不要切换、适不适合长期持有、投资价值怎么样；
  - 适合我买什么、结合我的目标/风险/持仓/成本做推荐、仓位控制、解套、割肉或加仓；
  - 消息面、题材发酵、客户占比、供应链关系、商业模式和估值逻辑分析。
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
- 纯条件选股、纯行情查询、客服问题、图片搜索或不需要投资分析的简单事实查询；
- 只看最终答案、完全不需要链路归因的轻量 benchmark。

若用户问题混合了筛选、分析和推荐，以用户是否要求解释、判断、评价、个人化适配或决策支持为准。若问题明显属于专门的 KYC 推荐建议评测，也可优先使用 `05-kyc-recommendation-suggestions`；本 skill 仍需覆盖分析评价中夹带的“适合我/我的持仓/我的风险目标”类质量缺口。

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

### 上下文与链路结构

- `context` 中的历史提问、历史持仓、画像、风险偏好、成本、期限或用户自述，是分析评价类问题的重要输入；
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
   阅读 [references/rubric/_index.md](references/rubric/_index.md)、[references/rubric/expert_answer_patterns.md](references/rubric/expert_answer_patterns.md) 和 [references/golden_cases/_index.md](references/golden_cases/_index.md)。
   仅根据 `question`、必要 `context` 和已提供的 `online_dimension_signals` 判断本题评价需求、证据需求、时效强度、决策强度、用户画像强度和场景/情绪强度。
   从种子维度池选择适用维度；若线上数据暴露的关键缺口无法被现有维度清楚覆盖，可新增运行时维度。
   同一题下，自研与竞品必须使用**同一套**适用性、运行时维度和权重，避免把权重差异误当成模型差异。
   对活跃维度判断适用性：
   - `relevant`：本题核心判断依据；
   - `supplementary`：有参考价值但不是主矛盾；
   - `not_applicable`：该维度与题目类型无关，跳过评分。
   动态权重总和必须为 100。权重分配记录到输出的 `weight_assignment`，新增运行时维度记录到 `runtime_dimensions`。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md)，判断用户问题是否命中专家案例或同类语义。命中时必须用对应 hard checks 作为核验清单。

1. **先分别做绝对评分**
   对自研与竞品分别按本 skill 定义的分析评价类维度评分，种子维度包括：
   - `intent_scenario_recognition`
   - `evidence_source_quality`
   - `recency_time_boundary`
   - `investment_logic_depth`
   - `method_fit`
   - `comparison_quantification`
   - `actionability_risk`
   - `user_profile_suitability`
   - `scenario_emotion_recognition`
   - `composition_credibility`
   - `tool_usage`

   若步骤 0 新增运行时维度，也必须对双方使用同一运行时维度评分。
   除 `tool_usage` 外，先只依据用户问题、必要上下文和各自最终答案评分；不得因为另一方更差，就抬高本方绝对分。每个活跃维度的 `raw_score` 必须取六档值：0/20/40/60/80/100。

2. **再分别诊断两边整体链路**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)、[references/tool_list/_index.md](references/tool_list/_index.md) 和 [references/whole_chain_comparison.md](references/whole_chain_comparison.md)。
   对两边分别检查：
   - 是否正确识别投资场景、用户真实决策需求和必要上下文；
   - 工具选择是否正确；
   - 查询输入是否贴合标的、资产、时间窗口、证据类型和用户目标；
   - 证据是否覆盖了题目真正需要的催化、基本面、估值、交易面、风险和用户画像维度；
   - 是否有交叉验证；
   - 工具结果是否真正转化成了更好的最终答案。

   当 `plan` 存在时，可结合其判断意图和推理；当 `plan` 为空时，不强行编造“推理文本”归因，优先依据工具行为、证据流和最终答案做判断。
   若题目要求“适合我”、结合风险目标、持仓成本、浮盈浮亏、迷茫或套牢处境，必须检查两边链路是否读取或使用了可见画像/历史上下文；没有可用画像时，最终答案是否明确说明依据不足并用分层假设、低风险边界或必要追问处理。
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
   - **证据优先**：每条优势、弱点和学习点都要绑定最终答案或链路证据；
   - **不做多模型聚合**：本协议一次只比较一个竞品，跨竞品总结由后续汇总层完成。

5. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 自研与竞品使用同一维度、同一权重、同一 hard checks；
- 不因为相对胜负而改变绝对评分；
- 不因为链路看起来繁复就自动加分；
- 若链路更好但最终答案没有兑现，优点只能记为链路信号，不能替代答案质量；
- 若双方都没有真正完成用户任务，必须明确输出共同不足，不能把“谁稍微好一点”写成高质量答案。
- 投资分析类问题优先评估是否抓住核心投资逻辑、关键证据、时间边界和可执行判断。
- 先判断答案是否贴近用户真实交易心理：消息面和题材问题看能否帮用户理解当下能不能赚钱、逻辑是否变了、资金为什么选/不选；不要把科普、资讯稿或低密度长答案当成好答案。
- 涉及个人化推荐时，先评估是否理解“人”和“处境”，再评估标的逻辑；不要把通用市场分析、热门标的清单或漂亮投顾模板当成私人化建议。
- 对浮亏、腰斩、迷茫、买什么都亏等场景，优先检查是否先降风险、稳住决策框架、给仓位/复盘/证伪条件；直接推荐短线、抓反弹或高波动主题应重扣。
- 对模板化、数据堆砌、技术指标错用、旧消息冒充最新消息保持严格扣分。
- 证据不足时可以低置信归因，但不要假装已经验证事实。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
