---
name: financial-performance-interpretation
description: 用于评测自研模型在财报业绩解读场景中的最终答案和完整链路质量。适用于年报、季报、业绩快报、分红公告、现金流、毛利率、ROE、营收确认、净利润差异、会计差错更正、投资性房地产公允价值、经营归因、股价影响和持续性判断等问题；输入包括用户 query、上下文、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 财报业绩解读评测协议

用稳定协议评测我方模型在财报业绩解读中的表现。以用户问题和最终答案 `text_answer` 为评分主锚点，以完整链路数据用于工具评分和根因归因。

## 适用范围

仅在用户问题属于财报、业绩公告、经营指标、会计口径或财务影响解释时使用，包括：
- 年报、季报、业绩快报、业绩预告、分红公告、官网公告的内容解读
- 营收、净利润、扣非净利润、毛利率、ROE、现金流、负债、偿债能力、收入确认等指标变化原因
- 财报利好/利空、业绩对股价影响、持续性、估值与市场预期判断
- 会计差错更正、收入确认政策变更、非经常性损益、公允价值变动、套期保值、税务补缴等特殊事件解释
- 将财务数据与真实业务、行业周期、价格、订单、成本、产品结构、政策或公司公告原文连接起来

不适用于纯条件选股、普通资讯问答、无财务报告语境的个股诊断、KYC 投顾建议或同花顺产品客服问答。

## 期望输入

每次评测获取：
- 用户问题 `question`
- 我方最终答案，优先使用 `text_answer`
- 完整对话上下文 `context`
- 完整规划链路 `chain`，包括 `plan`、工具调用、工具输入和工具输出
- 可用工具清单 `tools`

## 执行协议

0. **分析题目与分配动态权重**  
   阅读 [references/rubric/_index.md](references/rubric/_index.md) 和 [references/golden_cases/_index.md](references/golden_cases/_index.md)。仅根据用户问题判断每个维度适用性：`relevant` / `supplementary` / `not_applicable`。动态权重总和必须为 100，并写入 `weight_assignment`。命中专家案例或同类语义时，必须使用对应 hard checks；未命中具体案例时，也要使用 golden cases 文件末尾的跨案例判分锚点。

1. **盲评最终答案**  
   以 `text_answer` 为主锚点评分，不因为隐藏链路更好而给最终答案加分。对所有活跃维度输出 `raw_score` 和 `evidence`；不要计算加权分、总分或最终分数。`tool_usage` 例外，在步骤 2 评分。

2. **链路诊断和根因归因**  
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)，再阅读 [references/tool_list/_index.md](references/tool_list/_index.md)。用 `chain.plan` 判断意图和推理，用 `chain.tools[*].input/output` 判断工具选择、输入质量、公告全文获取、结构化财务数据查询和交叉验证。此时评分 `tool_usage`，并将其 `raw_score` 和 `evidence` 补入步骤 1 已输出的 `dimension_scores` 对象。根因必须绑定证据。

3. **应用封顶规则**  
   按需读取 [references/rubric/](references/rubric/_index.md) 中的 `cap_*.md` 文件。封顶规则限制最终分，不替代维度评分。多个封顶同时触发时取最低上限。

4. **序列化输出**  
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出结构化 JSON，再附简短自然语言评审。

## 保守评分

- 最终答案决定用户侧质量，链路只用于归因。
- 财报题不是背公式。好答案必须做到"事实锚点 + 科目变化 + 业务/会计原因 + 财务影响 + 可持续性或投资含义"。
- 用户问"为什么"时，不能只解释 ROE、现金流、毛利率的公式；必须回答这家公司这个报告期到底发生了什么。
- 用户前提错误时必须纠偏，例如把全年亏损、累计报表、调整前数据、单季数据或收入/利润口径混淆。
- 强制检查公告全文和特定披露。很多核心答案藏在年报附注、季报变动原因、会计差错更正公告、分红公告、官网公告、问询函或业绩说明会中。
- 能用公司披露原文或明确金额回答时，不要退化为泛化财务推理。截图中的坏答案常见模式是推理合理但没命中官方根因。
- 评价股价影响时必须区分短期情绪、已反映程度、基本面持续性、估值锚和观察指标；不要把主观预测包装成确定结论。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
