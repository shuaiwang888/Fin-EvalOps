# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。它只负责建立同题共享的评测框架，不做胜负判断。

## 1. 题目与配对校验

说明：
- `case_id` 是否配对到同一问题；
- 两边是否回答同一用户问题；
- 本题是否适用分析评价类自研 vs 竞品比较评测协议。

## 2. 维度适用性判断

逐个种子维度说明共享适用性级别及其理由：
- `relevant`
- `supplementary`
- `not_applicable`

格式示例：
```text
- intent_scenario_recognition: relevant — 两边都需要识别用户真实投资场景和决策需求
- user_profile_suitability: relevant — 用户明确要求结合持仓成本和风险偏好给建议
- scenario_emotion_recognition: supplementary — 用户有亏损焦虑信号，但不是本题主矛盾
```

若根据 `online_dimension_signals` 或本题关键缺口新增运行时维度，必须单独说明：
```text
- runtime dimension: business_purity — 本题需要判断题材与标的主营业务的真实相关度，种子维度无法单独承载该缺口
```

## 3. 共享权重分配方案

为所有活跃维度分配整数权重，总和必须为 100。自研和竞品必须共用这套权重。

```text
| 维度 | 权重 | 理由 |
|------|------|------|
| intent_scenario_recognition | 12 | 用户核心诉求是判断当前投资处境和决策任务 |
| investment_logic_depth | 18 | 需要把信息转化为核心投资逻辑和因果链 |
```

supplementary 维度通常保留低权重。若某个维度为 `not_applicable`，权重为 0，并写入后续 `skipped_dimensions`。

## 4. 两边证据摘要

分别记录：
- 自研最终答案中的亮点与缺陷；
- 竞品最终答案中的亮点与缺陷；
- 自研上下文/画像/持仓信息是否被答案使用；
- 竞品上下文/画像/持仓信息是否被答案使用；
- 自研整体链路中的关键工具/证据信号；
- 竞品整体链路中的关键工具/证据信号。

注意：
- 自研答案通常优先看 `text_answer`；
- 竞品若 `text_answer` 为空，则看 `answer`；
- 工具调用一律从 `chain[N].tools[M]` 读取，不从顶层 `tools` 猜测；
- 当竞品 `plan` 为空时，不要臆造不可见推理。

## 5. 绝对缺陷候选与比较焦点

分别列出两边可能触发的致命缺陷候选，格式：

```text
- self [missed_core_investment_logic]: 触发原因简述
- competitor [stale_or_wrong_time_evidence]: 触发原因简述
```

再列出后续最值得比较的 1-3 个焦点，例如：
- 谁真正完成了用户的投资决策任务；
- 谁抓住了核心投资逻辑、时效边界和关键证据；
- 谁把用户画像/持仓处境转化成了更合适的风险和行动建议；
- 谁的工具/证据链真正转化成了更好的最终答案。

如果未观察到明显缺陷，写明“未观察到明显致命缺陷”。
