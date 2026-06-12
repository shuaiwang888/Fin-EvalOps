---
name: instruction-following-ability-self-judge
description: 用于评测问财模型是否严格完成用户明确提出的任务、问题类型、约束和输出焦点。适用于用户有明确指令、任务类型或约束的金融问答；输入包括用户 query、context、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 指令遵循能力评测协议

用稳定协议评测问财模型是否严格完成用户明确提出的任务、问题类型、约束和输出焦点。评分以用户问题和最终答案（优先 `text_answer`）为核心；规划链路只用于工具使用评分和根因归因。

## 适用范围

适用于用户有明确指令、任务类型或约束的金融问答，例如：
- 问“原因/为什么”，答案必须解释驱动因素，不能只报涨跌数据。
- 问“定义/是什么”，答案必须先解释概念，不能只给指数、行情或查询结果。
- 问“截止某时点”“只看某范围”“不要某类”，答案必须遵守时间、范围、排除条件。
- 问“比较/区别/怎么选/排序”，答案必须按指定任务组织结论。

不适用于主要考察金融术语知识但没有明显指令偏离的问题；这些可使用金融常识与语义理解 skill。

## 期望输入

每次评测获取以下材料：
- 用户问题
- 我方最终答案，优先读取 `text_answer`
- 完整对话消息或规划链路
- 可见工具调用和工具输出

## 执行协议

0. **抽取指令与动态权重**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)。先从用户问题中抽取显式指令、隐含任务类型、约束条件和输出期望，再分配动态权重，总和必须为 100。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)，命中案例时使用对应 hard checks。

1. **逐项核验**
   阅读 [references/rubric/raw-score-scale.md](references/rubric/raw-score-scale.md)。仅对活跃维度按六档分制（0/20/40/60/80/100）打 raw score。先看答案是否完成指令，再看数据是否支持；不能因答案有相关数据而忽略指令缺失。

2. **诊断根因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md) 和按需的 L1 文件。`tool_usage` 维度读取 [references/tool_list/_index.md](references/tool_list/_index.md) 后评分。

3. **应用封顶规则**
   阅读 [references/rubric/](references/rubric/_index.md) 中对应的封顶规则文件。如果答案没有完成用户主指令，即使内容相关，也必须封顶。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出 JSON，再附简短自然语言评审。

## 安全护栏

- “原因”题必须解释原因，涨跌幅、资金流、成交额只是证据，不是原因本身。
- “定义”题必须给概念边界、常用标准和易混点，不能只给查询结果。
- 不要把可选补充信息放在核心指令前面，导致用户主问未被回答。
- 用户给出时间、对象、范围、排除项时，必须逐项核对。
- 若答案完成了相关任务但不是用户要求的任务，应按答非所问处理。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
