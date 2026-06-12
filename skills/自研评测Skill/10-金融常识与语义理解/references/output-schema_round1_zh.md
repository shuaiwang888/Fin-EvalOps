# Round 1 分析输出格式

Round 1 的输出为**自然语言分析报告**，不是 JSON。按以下小节组织内容。

## 1. 维度适用性判断

逐个维度说明适用性级别及其理由：

- **relevant**：该维度对本题目的评测至关重要，必须重点考察
- **supplementary**：该维度有参考价值但不是核心，权重较低（一般 3-10）
- **not_applicable**：该维度与本题完全无关，不参与评分

格式示例：
```
- semantic_intent_alignment: relevant — 用户有明确的金融语义理解需求
- entity_product_boundary: supplementary — 本题不涉及复杂的实体或产品边界区分
- metric_caliber_accuracy: not_applicable — 本题未涉及指标口径
```

## 2. 权重分配方案

为所有活跃维度（relevant + supplementary）分配整数权重，总和必须为 100。

用表格列出每个活跃维度的分配权重和理由：

```
| 维度 | 权重 | 理由 |
|------|------|------|
| semantic_intent_alignment | 25 | 用户语义意图是本题核心评测维度 |
| financial_term_understanding | 20 | 需要评估对金融术语的理解 |
| ... | ... | ... |
```

supplementary 维度权重一般 3-10。

## 3. 关键证据摘要

从题目、答案、规划链路（chain）中观察到的关键信号。包括：
- 用户问题的核心金融语义约束
- 答案中表现突出的亮点
- 答案中明显的缺陷或遗漏
- 工具调用链路中的关键节点

## 4. 致命缺陷候选

初步识别可能触发的 cap label 项，格式：

```
- [label_tag]: 触发原因简述
```

如果未观察到致命缺陷，写明"未观察到致命缺陷"。
