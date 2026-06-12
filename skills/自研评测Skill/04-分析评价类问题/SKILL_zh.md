---
name: analysis-evaluation-and-self-judgment
description: 用于评测自研模型在股票、基金、指数、宏观资产等分析评价类问题上的最终答案和完整链路质量。适用于自动审稿、动态权重评分、问题定位和根因归因，输入包括用户 query、上下文、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 分析评价类问题评测协议

用稳定协议评测我方模型在分析评价类金融问答中的表现。以用户问题和最终答案 `text_answer` 为评分主锚点，以完整链路数据用于解释问题发生在哪里。

## 适用范围

仅在用户问题属于分析评价类时使用，包括：
- 股票、指数、基金、ETF、宏观资产的分析、评价、诊断、趋势判断
- 为什么上涨、为什么没涨、为什么冲高回落等行情归因
- 能不能买、要不要切换、适不适合长期持有、投资价值怎么样
- 适合我买什么、结合我的目标/风险/持仓/成本做推荐、仓位控制、解套、割肉或加仓
- 消息面、题材发酵、客户占比、供应链关系、商业模式和估值逻辑分析

不用于纯条件选股、纯行情查询、客服问题、图片搜索或不需要投资分析的简单事实查询。若用户问题混合了筛选、分析和推荐，以用户是否要求解释、判断、评价、个人化适配或决策支持为准。若问题明显属于专门的 KYC 推荐建议评测，也可优先使用 `05-kyc-recommendation-suggestions`；本 skill 仍需覆盖分析评价中夹带的“适合我/我的持仓/我的风险目标”类质量缺口。

## 期望输入

每次评测获取以下材料：
- 用户问题 `question`
- 我方最终答案，优先使用 `text_answer`
- 完整对话上下文 `context`，包括历史提问、历史持仓/偏好、画像或用户自述
- 完整规划链路 `chain`，包括 `plan`、工具调用、工具输入和工具输出
- 可用工具清单 `tools`
- 可选线上维度信号 `online_dimension_signals`，如近期线上失败样本、用户反馈、人工标注摘要或维度统计

## 执行协议

0. **识别评价需求并分配动态权重**
   先阅读 [references/rubric/_index.md](references/rubric/_index.md)、[references/rubric/expert_answer_patterns.md](references/rubric/expert_answer_patterns.md) 和 [references/golden_cases/_index.md](references/golden_cases/_index.md)。
   仅根据 `question`、必要 `context` 和已提供的 `online_dimension_signals` 判断本题评价需求、证据需求、时效强度、决策强度、用户画像强度和场景/情绪强度。
   不要先把问题强行归入固定题型；题材、基金、宏观、消息面等主题只作为检索专家案例和 hard checks 的线索。
   从种子维度池选择适用维度；若线上数据暴露的关键缺口无法被现有维度清楚覆盖，可新增运行时维度。
   对活跃维度判断适用性：
   - `relevant`：本题核心判断依据
   - `supplementary`：有参考价值但不是主矛盾
   动态权重总和必须为 100。权重分配记录到输出的 `weight_assignment`，新增运行时维度记录到 `runtime_dimensions`。
   - `not_applicable`（不适用）：该维度与题目类型无关，跳过评分
   根据适用性分配动态权重（总和必须 = 100）：
   - `relevant` 维度获得较高权重（从 `not_applicable` 维度让出权重）
   - `supplementary` 维度保留低权重（建议 3-5）
   - `not_applicable` 维度权重 = 0，评分阶段直接跳过
   将权重分配记录到输出的 `weight_assignment` 中。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md)，判断用户问题是否命中专家案例或同类语义。命中时必须用对应 hard checks 作为核验清单。

1. **盲评最终答案**
   以 `text_answer` 为主锚点评分，不因为隐藏链路更好而给最终答案加分。
   对所有 `relevant` 和 `supplementary` 维度输出 `raw_score`，不要计算加权分或总分。
   例外：`tool_usage` 需要阅读链路，在步骤 2 中评分。

2. **链路诊断和根因归因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)。
   再阅读 [references/tool_list/_index.md](references/tool_list/_index.md)，按需读取具体工具规则。
   用 `chain.plan` 判断意图理解、画像/上下文处理和推理过程，用 `chain.tools[*].input/output` 判断工具选择、输入质量、证据质量和是否误读工具结果。
   若题目要求“适合我”、结合风险目标、持仓成本、浮盈浮亏、迷茫或套牢处境，必须检查链路是否读取或使用了可见画像/历史上下文；没有可用画像时，最终答案是否明确说明依据不足并用分层假设、低风险边界或必要追问处理。
   此时评分 `tool_usage`。
   根因必须回答：如果答案不好，具体不好在哪，问题发生在理解、证据、工具、推理、表达还是能力/数据源缺口。

3. **应用封顶规则**
   按需读取 [references/rubric/](references/rubric/_index.md) 中的 `cap_*.md` 文件。
   封顶规则限制最终分，不替代维度评分。若多个封顶同时触发，取最低上限。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 最终答案决定用户侧质量，链路只用于归因。
- 不要把“有表格、有很多指标、有工具调用”自动视为高质量。
- 投资分析类问题优先评估是否抓住核心投资逻辑、关键证据、时间边界和可执行判断。
- 先判断答案是否贴近用户真实交易心理：消息面和题材问题看能否帮用户理解当下能不能赚钱、逻辑是否变了、资金为什么选/不选；不要把科普、资讯稿或低密度长答案当成好答案。
- 涉及个人化推荐时，先评估是否理解“人”和“处境”，再评估标的逻辑；不要把通用市场分析、热门标的清单或漂亮投顾模板当成私人化建议。
- 对浮亏、腰斩、迷茫、买什么都亏等场景，优先检查是否先降风险、稳住决策框架、给仓位/复盘/证伪条件；直接推荐短线、抓反弹或高波动主题应重扣。
- 对模板化、数据堆砌、技术指标错用、旧消息冒充最新消息保持严格扣分。
- 证据不足时可以低置信归因，但不要假装已经验证事实。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
