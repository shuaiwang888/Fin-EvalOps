# L1: `intent`

用于归因模型没有正确理解用户的推荐任务或决策需求。

常见 L2：
- `missed-personal-suitability-intent`：用户要求“适合我”，模型按通用推荐处理。
- `wrong-decision-task`：用户问持有/加仓/割肉，模型写成普通分析。
- `missed-allocation-objective`：用户要资产配置或方向取舍，模型只罗列标的。
- `over-narrowed-or-over-broadened-intent`：把宽配置问题缩成单一标的，或把具体买卖问题泛化成宏观讨论。

证据要求：
- 引用 `question` 中的意图表达。
- 引用 `text_answer` 中未响应或错误响应的部分。
