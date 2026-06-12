# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。它只负责建立同题共享的评测框架，不做胜负判断。

## 1. 题目与配对校验

说明：
- `self_case_id` 与 `competitor_case_id` 是否配对到同一问题；
- 两边是否回答同一用户问题和同一上下文；
- 本题是否适用交互澄清自研 vs 竞品比较评测协议。

## 2. 维度适用性判断

逐个维度说明共享适用性级别及其理由：
- `relevant`
- `supplementary`
- `not_applicable`

必须覆盖本 skill 的 11 个维度：
- `intent_fulfillment`
- `ambiguity_clarification`
- `context_continuity`
- `entity_resolution`
- `financial_rule_and_premise`
- `assumption_definition`
- `actionability_and_risk_plan`
- `evidence_grounding`
- `guidance_and_retention`
- `tool_usage`
- `latency_efficiency`

格式示例：

```text
- ambiguity_clarification: relevant — 用户缺少成本、仓位和时间目标，不能直接给回本方案
- context_continuity: supplementary — 输入含历史轮次，但本轮未明确要求承接前轮承诺
- entity_resolution: not_applicable — 标的名称清楚，无错别字、代码异常或简称歧义
```

## 3. 共享权重分配方案

为所有活跃维度分配整数权重，总和必须为 100。自研和竞品必须共用这套权重。

```text
| 维度 | 权重 | 理由 |
|------|------|------|
| ambiguity_clarification | 20 | 题目核心是判断能否直接回答并问到关键变量 |
| financial_rule_and_premise | 18 | 用户问题包含交易规则或错误前提 |
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
- 工具调用一律从 `chain[N].tools[M]` 读取，不从顶层 `tools` 猜测；
- 竞品 `plan` 为空时，不臆造不可见推理。

## 5. 绝对缺陷候选与比较焦点

分别列出两边可能触发的致命缺陷候选；再列出后续最值得比较的 1-3 个焦点，例如：
- 谁真正识别了必须澄清的关键变量；
- 谁更好承接用户补充信息；
- 谁更准确处理错别字、异常代码或多义标的；
- 谁更准确纠正交易规则或错误前提；
- 谁的工具/证据链真正转化成了更好的最终答案。

如果未观察到明显缺陷，写明“未观察到明显致命缺陷”。
