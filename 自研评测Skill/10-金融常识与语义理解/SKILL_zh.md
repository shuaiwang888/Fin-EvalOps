---
name: financial-common-sense-and-semantic-understanding-self-judge
description: 用于评测问财模型在金融常识、术语、交易规则、实体边界、指标口径和语义理解方面的回答质量。适用于金融概念解释、指标口径判断、实体/产品识别、错别字/黑话纠错和语义关联类问题；输入包括用户 query、context、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 金融常识与语义理解评测协议

用稳定协议评测问财模型回答中对金融概念、术语、交易规则、实体边界和数据口径的理解是否准确。评分以用户问题和最终答案（优先 `text_answer`）为核心；规划链路只用于工具使用评分和根因归因。

## 适用范围

适用于金融常识、金融语义理解、指标口径、交易规则、实体识别和用户真实意图补全类问题，例如：
- 财务/资金指标术语解释、量化筛选和口径判断：现金奶牛、净利润断层、主力控盘、PE 最小、最新季度 ROE。
- 交易规则和市场制度理解：集合竞价、盘中最新价、ST 与 *ST、财报披露期。
- 金融实体和产品边界：黄金现货 vs 黄金 ETF、基金公司 vs 旗下基金、豪威集团 vs 豪能股份。
- 错别字、黑话、俚语、新题材和含混问法的语义纠错：心质/新质生产力、Token、老登股、敢死队。
- 行业/个股/基金之间的语义关联：重仓半导体封测个股的 ETF、易方达基金表现。

不适用于主要考察事件选股排序、严格指令遵循或复杂投资逻辑推理的题目；这些分别使用对应 skill。

## 期望输入

每次评测获取以下材料：
- 用户问题
- 我方最终答案，优先读取 `text_answer`
- 完整对话消息或规划链路
- 可见工具调用和工具输出

## 执行协议

0. **分析题目与分配动态权重**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)，仅基于用户问题判断各维度适用性：`relevant` / `supplementary` / `not_applicable`。动态权重总和必须为 100。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)，判断是否命中专家案例或图片批注锚点。命中时必须使用对应 hard checks。

1. **盲评打分**
   阅读 [references/rubric/raw-score-scale.md](references/rubric/raw-score-scale.md)。仅对 `relevant` 和 `supplementary` 维度按 0-5 整数打 raw score，并给出证据。不要计算加权分、总分或最终分。

2. **诊断根因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)，按需读取 `intent`、`evidence`、`tool`、`reasoning`、`composition` 五类根因文件。
   `tool_usage` 维度需要阅读规划链路和 [references/tool_list/_index.md](references/tool_list/_index.md) 后评分。

3. **应用封顶规则**
   阅读 [references/rubric/](references/rubric/_index.md) 中对应的封顶规则文件。若答案出现硬性概念误判、实体错配、交易规则错误、关键口径错误或答非所问，按最低适用上限封顶。封顶不替代维度评分。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出结构化 JSON，再附简短自然语言评审。

## 安全护栏

- 不要把相似金融产品混为一谈；现货、ETF、基金、指数、股票、基金公司和旗下基金要分清。
- 不要用模型自造指标替代市场共识；若使用自定义指标，必须解释定义、口径和局限。
- 对错别字和黑话要推断真实意图，但不能无证据强行联想。
- 对“最新”“近期”“当下价格”“盘中”等时间词要使用正确时点和披露周期。
- 对 PE、ROE、ST、集合竞价等基础规则，硬性错误应重扣。
- 数据表只能支撑答案，不能代替概念解释和语义判断。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
