# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。它只负责建立同题共享的评测框架，不做胜负判断。

## 1. 题目与配对校验

说明：
- `case_id` 是否配对到同一问题；
- 两边是否回答同一用户问题；
- 本题是否适用金融逻辑推理最终回答比较评测协议。

## 2. 共享决策任务解析

从用户问题中抽取：
- `task_type`：`stock_selection | trend_forecast | operation_advice | comparison | risk_scenario`；
- `decision_object`：用户指定股票、板块、概念、行业或股票池；
- `time_horizon`：明天、下周、近期、长期、截至某日或未指定；
- `required_reasoning_focus`：题目最需要的推理焦点，例如热点催化、资金承接、技术形态、基本面、估值、安全边际、情景风险等。

示例：
```text
- task_type: stock_selection
- decision_object: 用户要求筛选便宜且有潜力的股票
- time_horizon: 近期
- required_reasoning_focus: 估值不能只看低 PE，需要结合增长、景气、催化和资金逻辑
```

## 3. 维度适用性判断

逐个维度说明共享适用性级别及其理由：
- `relevant`
- `supplementary`
- `not_applicable`

格式示例：
```text
- financial_logic_chain: relevant - 需要从事实和指标推导投资结论
- market_driver_identification: relevant - 用户问短线强势，需识别热点和题材发酵
- scenario_risk_reasoning: supplementary - 用户没有明确要求风险推演，但预测题仍需给风险边界
```

## 4. 共享权重分配方案

为所有活跃维度分配整数权重，总和必须为 100。自研和竞品必须共用这套权重。

```text
| 维度 | 权重 | 理由 |
|------|------|------|
| financial_logic_chain | 25 | 用户需要完整投资逻辑 |
| evidence_to_conclusion | 25 | 证据必须支撑预测或排序结论 |
```

## 5. 两边最终回答证据摘要

分别记录：
- 自研最终回答中的亮点与缺陷；
- 竞品最终回答中的亮点与缺陷；
- 哪些最终回答片段体现了金融逻辑链、市场驱动、证据支撑、比较排序、情景风险和决策表达；
- 哪些判断只能从过程字段看到、不能作为本轮评分依据。

注意：
- 自研答案优先看 `self_record.text_answer`；若为空，可看 `self_record.answer`；
- 竞品答案优先看 `competitor_record.text_answer`；若为空，可看 `competitor_record.answer`；
- 证据只能回指用户问题或双方最终回答；
- 摘要必须围绕金融逻辑链、市场驱动、证据支撑、比较排序、情景风险和决策表达，不要只罗列数据。

## 6. 绝对缺陷候选与比较焦点

分别列出两边可能触发的致命缺陷候选；再列出后续最值得比较的 1-3 个焦点，例如：
- 谁真正形成了金融逻辑链；
- 谁抓住了市场驱动；
- 谁把证据转化成了更可靠的结论；
- 谁的比较标准、风险边界和决策表达更可用。

如果未观察到明显缺陷，写明“未观察到明显致命缺陷”。
