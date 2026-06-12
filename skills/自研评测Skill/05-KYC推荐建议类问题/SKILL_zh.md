---
name: kyc-recommendation-suggestions
description: 用于评测自研模型在 KYC 推荐建议类金融问题上的最终答案和完整链路质量。适用于标的推荐、基金/ETF 推荐、买卖持仓建议、资产配置、解套加仓减仓、结合用户风险目标的投顾式决策支持，输入包括用户 query、context 历史提问、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# KYC 推荐建议类问题评测协议

用稳定协议评测我方模型在 KYC 推荐建议类问题上的表现。以用户问题和最终答案 `text_answer` 为评分主锚点，以完整链路数据用于解释问题发生在哪里。05 类问题的默认标准是：自研模型应主动使用用户 KYC 数据进行回答；若没有使用，应评测出“理当使用 KYC，但实际未使用，导致推荐适配性变差”的问题点。

## 适用范围

仅在用户问题属于投资推荐、配置建议或交易决策支持时使用，包括：
- 推荐适合我的股票、基金、ETF、行业、资产或组合
- 能不能买、是否继续持有、该割肉还是加仓、怎么控制仓位
- 结合我的目标、风险、资金、持仓、风格给建议
- 宏观/行业/市场情景下的方向选择、资产比较和配置顺序
- 用户处于浮亏、套牢、迷茫、信心受挫等真实投资处境时的投顾式建议

不用于纯行情查询、纯事实查询、客服问题、图片搜索或不需要用户适配的普通资料总结。若问题同时包含分析和推荐，以是否需要给用户做适配后的决策建议为准。

## 期望输入

每次评测获取以下材料：
- 用户问题 `question`
- 我方最终答案，优先使用 `text_answer`
- 历史对话或历史提问 `context`
- 完整规划链路 `chain`，包括 `plan`、工具调用、工具输入和工具输出
- 可用工具清单 `tools`
- 用户画像信息 `meta.user_investment_goal`（若存在）：包含用户风险承受能力、投资目标、投资周期、分析方法、投资理念等，是评测员判断模型是否主动使用 KYC 数据、推荐是否针对该用户适配的关键参考
- 可选线上维度信号 `online_dimension_signals`，如近期线上失败样本、用户反馈、人工标注摘要或维度统计

当前 v1 对 05 类问题采用强 KYC 标准：只要用户问题属于投资推荐、配置建议或交易决策支持，就应检查模型是否主动获取并使用用户 KYC 数据。KYC 数据可以来自用户画像工具、用户画像存储、历史 `context`、当前问题中的自述信息或链路中可见的画像检索结果。不要把“context 中没有 KYC”作为放过模型的理由；关键是模型面对这类问题时是否遵循“先取 KYC、再做推荐”的标准。

## 执行协议

0. **识别推荐场景并分配动态权重**
   先阅读 [references/rubric/_index.md](references/rubric/_index.md) 和 [references/golden_cases/_index.md](references/golden_cases/_index.md)。
   仅根据 `question`、必要 `context` 和已提供的 `online_dimension_signals` 判断本题推荐目标、KYC 强度、证据需求、决策强度和风险责任。
   对 05 类适用问题，KYC 强度至少为 relevant：即使问题只写“推荐一下”“该不该买”“怎么配置”，只要答案会形成个人投资建议，就应评估模型是否主动使用用户 KYC 数据。
   不要先把问题强行归入固定题型；股票、基金、ETF、宏观资产、行业方向只是检索专家案例和 hard checks 的线索。
   对维度判断适用性：
   - `relevant`：本题核心判断依据
   - `supplementary`：有参考价值但不是主矛盾
   - `not_applicable`：该维度与题目无关，跳过评分
   动态权重总和必须为 100，并记录到输出的 `weight_assignment`。若线上数据暴露的关键缺口无法被现有维度清楚覆盖，可新增临时评分维度，并直接并入 `weight_assignment` 与 `dimension_scores`。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md)，判断用户问题是否命中专家案例或同类语义。命中时必须使用对应 hard checks。
   若题目涉及“适合我”、ETF/基金推荐、亏损迷茫、持仓去留、宏观配置、多资产/多行业取舍、仓位控制、具体标的推荐或线上反馈“每次推荐不一样”，继续阅读 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)，使用截图人工批注沉淀的 hard checks。

1. **盲评最终答案**
   以 `text_answer` 为主锚点评分，不因为隐藏链路更好而给最终答案加分。
   需要判断最终答案是否体现用户 KYC 数据对推荐结论的约束，例如风险承受能力、投资期限、资金目标、持仓背景、交易经验、偏好或历史亏损处境。若提供了 `meta.user_investment_goal`，必须将答案与该画像对照：画像明确给出的风险偏好、投资目标、投资周期等应与推荐结论一致；若答案推荐了明显不匹配用户画像的产品或策略（如向保守型用户推荐高波动标的），应在画像理解、适当性等维度扣分。
   若答案只给通用推荐、热门标的或模板组合，应在画像理解、适当性、风险边界等维度扣分。
   对所有 `relevant` 和 `supplementary` 维度输出 `raw_score`，不要计算加权分或总分。
   例外：`tool_usage` 需要阅读链路，在步骤 2 中评分。

2. **链路诊断和根因归因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)。
   再阅读 [references/tool_list/_index.md](references/tool_list/_index.md)，按需读取具体工具规则。
   用 `chain.plan` 判断意图理解、KYC 画像处理和推理过程，用 `chain.tools[*].input/output` 判断工具选择、输入质量、证据质量和是否误读工具结果。
   必须专门检查链路是否有读取、调用、检索或引用用户 KYC 数据的动作。若提供了 `meta.user_investment_goal`，该画像即为此题的 KYC 基准——评测员应检查链路的 `plan` 和工具调用中是否出现了与画像内容匹配的 KYC 读取或引用。若链路没有，而最终答案又形成了推荐或交易建议，应归因为 `context` / `tool` / `reasoning` 中的 KYC 使用缺失，并在根因 summary 中明确写出”应使用用户 KYC 数据但未使用”。
   此时评分 `tool_usage`。
   根因必须回答：如果答案不好，具体不好在哪，问题发生在意图理解、上下文使用、证据、工具、推理、表达还是安全合规边界。

3. **应用封顶规则**
   按需读取 [references/rubric/](references/rubric/_index.md) 中的 `cap_*.md` 文件。
   封顶规则限制最终分，不替代维度评分。若多个封顶同时触发，取最低上限。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。
   先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 最终答案决定用户侧质量，链路只用于归因。
- 不要把“给了很多标的、很多指标、很多工具调用”自动视为高质量。
- KYC 推荐建议优先评估是否先理解人和场景，再决定推荐、仓位、期限和风险边界。
- “私人投顾感”是 05 类的重要质量标准：答案要让用户看出模型知道我是谁、我处在什么投资状态、为什么这个建议适合我，而不是只给市场观点或产品榜单。
- 对 05 类问题，高质量答案应主动使用用户 KYC 数据。若链路没有取到 KYC，也应在答案中说明画像依据不足，并给出分层、条件化、低风险边界清晰的建议或必要追问；不能直接当作普通市场问答处理。
- 严惩编造用户画像、忽略亏损/迷茫/套牢情绪、把高风险短线策略推荐给明显不适配的用户。
- 对模板化荐股、窄行业高波动推荐、同类问题推荐不稳定且无解释、过度确定的底部/收益判断、关键数据缺失保持严格扣分。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。工具列表直接复用事件概念选股 skill 的工具定义，当前复制在 [references/tool_list/_index.md](references/tool_list/_index.md)。
