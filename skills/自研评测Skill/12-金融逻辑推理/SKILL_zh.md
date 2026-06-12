---
name: financial-logical-reasoning-self-judge
description: 用于评测问财模型在投资逻辑推理、市场驱动识别、证据到结论连接、多股比较和风险推演方面的回答质量。适用于投资判断、走势预测、个股选择、强势股筛选、板块内比较和风险情景推演类问题；输入包括用户 query、context、plan、工具调用输入输出和最终回答，输出与 self_judge 体系一致的 JSON 评测结果。
---

# 金融逻辑推理评测协议

用稳定协议评测问财模型是否能把金融事实、市场驱动、个股属性、资金/技术/基本面证据推导成有决策价值的结论。评分以用户问题和最终答案（优先 `text_answer`）为核心；规划链路只用于工具使用评分和根因归因。

## 适用范围

适用于投资判断、走势预测、个股选择、强势股筛选、板块内比较和风险情景推演类问题，例如：
- 便宜有潜力的股票、明天可能涨停的股票。
- 个股下周走势、还能不能追、后市怎么操作。
- 多只概念股怎么选、谁弹性更强、谁更稳健。
- 根据市场热点、资金、技术面、基本面和事件催化形成投资逻辑。

不适用于只考察单个金融术语定义或单纯指令未遵循的问题；这些使用对应 skill。

## 期望输入

每次评测获取以下材料：
- 用户问题
- 我方最终答案，优先读取 `text_answer`
- 完整对话消息或规划链路
- 可见工具调用和工具输出

## 执行协议

0. **识别决策任务与动态权重**
   阅读 [references/rubric/_index.md](references/rubric/_index.md)，判断题目需要预测、筛选、比较、排序、操作建议还是风险推演。动态权重总和必须为 100。
   阅读 [references/golden_cases/_index.md](references/golden_cases/_index.md) 和 [references/golden_cases/image_annotation_anchors.md](references/golden_cases/image_annotation_anchors.md)，命中案例时使用 hard checks。

1. **盲评推理质量**
   阅读 [references/rubric/raw-score-scale.md](references/rubric/raw-score-scale.md)。仅对活跃维度按 0/20/40/60/80/100 六档打 raw score。判断证据是否真的支持结论，而不是只堆技术面、资金面或公告。

2. **诊断根因**
   阅读 [references/root-cause/_index.md](references/root-cause/_index.md)。`tool_usage` 维度读取规划链路和 [references/tool_list/_index.md](references/tool_list/_index.md) 后评分。

3. **应用封顶规则**
   阅读 [references/rubric/](references/rubric/_index.md) 中对应的封顶规则文件。若结论与证据脱节、关键市场驱动缺失、风险承诺过度或比较逻辑错误，按规则封顶。

4. **序列化输出**
   阅读 [references/output-schema_zh.md](references/output-schema_zh.md)。先输出 JSON，再附简短自然语言评审。

## 安全护栏

- 不要把单一指标当成完整投资逻辑；估值、资金、技术面、公告都需要解释“为什么影响未来”。
- “便宜”不等于 PE 为负；“有潜力”需要增长、景气、催化或资金逻辑。
- 预测类问题要给情景、条件和风险，不得保证涨停或确定收益。
- 多股比较要有统一标准，如业务占比、弹性、自给率、资金承接、估值、安全边际。
- 不能用八股文四大面堆砌替代重点分析。
- 对短线题，市场热点和题材发酵链路往往比静态指标更关键。

## 参考索引

通过 [references/MANIFEST.md](references/MANIFEST.md) 按需读取子文件。
