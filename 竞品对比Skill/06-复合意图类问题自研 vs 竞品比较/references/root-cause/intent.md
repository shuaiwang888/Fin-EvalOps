# L1: `intent`

用于归因模型没有正确拆解用户的复合意图。

常见 L2：
- `missed-subtask-extraction`：未抽取关键子任务。
- `missed-time-window`：忽略 48 小时、7 天、事件后、3 月内等时间窗口。
- `missed-output-format-or-object`：忽略用户要求的对象范围、行业/公司/合约或输出形式。
- `collapsed-multiple-intents`：把多个强子任务压成一个泛化主题。

证据要求：
- 引用 `question` 中被漏拆或错拆的表达。
- 引用 `text_answer` 中对应缺失或错误响应。
