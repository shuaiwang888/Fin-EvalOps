# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。它只负责建立同题共享的评测框架，不做胜负判断。

## 1. 题目与配对校验

说明：
- `case_id` 是否配对到同一问题；
- 两边是否回答同一用户问题；
- 本题是否适用指令遵循能力比较评测协议。

## 2. 共享指令解析

从用户问题中抽取：
- `primary_instruction`：用户主指令；
- `constraints`：时间、范围、对象、排除项、格式或其他显式约束；
- `expected_answer_type`：原因分析、定义解释、比较、排序、建议、核实、数据查询等；
- `secondary_information`：题中出现但不应喧宾夺主的辅助信息。

示例：
```text
- primary_instruction: 分析领涨原因
- constraints: 截止今天上午 9 点 36 分；赛马概念；海南橡胶也涨
- expected_answer_type: cause_analysis
- secondary_information: 涨幅、成交额、板块表现只能作为证据
```

## 3. 维度适用性判断

逐个维度说明共享适用性级别及其理由：
- `relevant`
- `supplementary`
- `not_applicable`

格式示例：
```text
- explicit_instruction_completion: relevant - 用户明确要求完成原因分析
- task_type_alignment: relevant - 原因分析不能替换成行情播报
- constraint_coverage: relevant - 题目包含时点、概念和个股约束
```

## 4. 共享权重分配方案

为所有活跃维度分配整数权重，总和必须为 100。自研和竞品必须共用这套权重。

```text
| 维度 | 权重 | 理由 |
|------|------|------|
| explicit_instruction_completion | 30 | 主指令非常明确 |
| task_type_alignment | 20 | 需要防止原因题被答成数据播报 |
```

## 5. 两边证据摘要

分别记录：
- 自研最终答案中的亮点与缺陷；
- 竞品最终答案中的亮点与缺陷；
- 自研整体链路中的关键工具/证据信号；
- 竞品整体链路中的关键工具/证据信号。

注意：
- 自研答案通常优先看 `text_answer`；
- 竞品若 `text_answer` 为空，则看 `answer`；
- 工具调用一律从 `chain[N].tools[M]` 读取，不从顶层 `tools` 猜测；
- 摘要必须围绕主指令、任务类型、约束覆盖和答案焦点，不要只罗列数据。

## 6. 绝对缺陷候选与比较焦点

分别列出两边可能触发的致命缺陷候选；再列出后续最值得比较的 1-3 个焦点，例如：
- 谁真正完成了用户主指令；
- 谁更准确对齐任务类型；
- 谁更完整遵守关键约束；
- 谁把工具结果转化成了用户要求的答案。

如果未观察到明显缺陷，写明“未观察到明显致命缺陷”。
