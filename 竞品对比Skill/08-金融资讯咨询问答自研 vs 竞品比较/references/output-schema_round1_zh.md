# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。它只负责建立同题共享的评测框架，不做胜负判断。

## 1. 题目与配对校验

说明：
- `self_case_id` 与 `competitor_case_id` 是否配对到同一问题；
- 两边是否回答同一用户问题；
- 本题是否适用金融资讯咨询问答自研 vs 竞品比较评测协议。

如果 `same_question_verified=false`，Round 2 不得继续输出胜负结论，只能说明无法比较。

## 2. 维度适用性判断

逐个维度说明共享适用性级别及其理由：
- `relevant`
- `supplementary`
- `not_applicable`

格式示例：

```text
- intent_fulfillment: relevant — 两边都需要完成用户显性问题和隐含投资诉求
- timeliness_fact_boundary: relevant — 用户问"最新/近期"政策动态，时间边界是核心
- fact_evidence_quality: relevant — 需要可靠事实、数据口径和来源类型支撑
- information_integration: supplementary — 单点查询也需要基本组织，但不是本题核心
- investment_mapping: relevant — 用户关心对行业和标的的影响
- core_signal_extraction: relevant — 需要抓住主要催化剂而非素材罗列
- nonstandard_source_awareness: supplementary — 问题可能涉及市场传闻、调研纪要或大 V 文章
- credibility_expression: supplementary — 表达可信度始终有参考价值
- tool_usage: relevant — 两边都提供完整链路，可比较工具使用策略
```

## 3. 共享权重分配方案

为所有活跃维度分配整数权重，总和必须为 100。自研和竞品必须共用这套权重。

```text
| 维度 | 权重 | 理由 |
|------|------|------|
| intent_fulfillment | 15 | 用户要求解释事件影响并给出判断 |
| timeliness_fact_boundary | 15 | 问题包含最新/近期/截至某日 |
| fact_evidence_quality | 15 | 需要可靠事实、数据口径和来源 |
```

## 4. 两边证据摘要

分别记录：
- 自研最终答案中的亮点与缺陷；
- 竞品最终答案中的亮点与缺陷；
- 自研整体链路中的关键工具/证据信号；
- 竞品整体链路中的关键工具/证据信号。

注意：
- 自研答案通常优先看 `text_answer`；
- 竞品若 `text_answer` 为空，则看 `answer`；
- 工具调用一律从 `chain[N].tools[M]` 读取，不从顶层 `tools` 猜测。

## 5. 绝对缺陷候选与比较焦点

分别列出两边可能触发的致命缺陷候选；再列出后续最值得比较的 1-3 个焦点，例如：
- 谁真正覆盖了用户显性问题和隐含投资诉求；
- 谁的时间窗口、事实边界、数据口径和事件进展更稳；
- 谁的证据更新、更权威、更贴近用户问题；
- 谁把资讯影响转化成了更可执行的投资映射；
- 谁抓住了市场真正交易的核心信号；
- 谁对非标准资讯来源的价值与边界处理更好；
- 谁的工具/证据链真正转化成了更好的最终答案。

如果未观察到明显致命缺陷，写明"未观察到明显致命缺陷"。
