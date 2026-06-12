# 评分细则索引

## 维度列表

| 维度 | 建议权重 | 适用性判断 |
|---|---:|---|
| [`explicit_instruction_completion`](explicit_instruction_completion.md) 显式指令完成 | 30 | 始终 relevant。主指令是否被完成 |
| [`task_type_alignment`](task_type_alignment.md) 任务类型对齐 | 20 | 始终 relevant。原因、定义、比较、排序、建议等任务类型是否对齐 |
| [`constraint_coverage`](constraint_coverage.md) 约束覆盖 | 15 | 用户有时间、范围、对象、排除条件时 relevant；否则 supplementary |
| [`answer_focus`](answer_focus.md) 答案焦点 | 15 | 始终 relevant。是否围绕主问展开，而非数据堆砌或跑题 |
| [`necessary_information_completeness`](necessary_information_completeness.md) 必要信息完整度 | 10 | 始终 supplementary；主指令需要证据链时 relevant |
| [`tool_usage`](tool_usage.md) 工具使用合理性 | 10 | 始终 relevant |

## 动态权重

- 先抽取 `primary_instruction`，再评估答案。
- 主指令越明确，`explicit_instruction_completion` 权重越高。
- 明确约束越多，`constraint_coverage` 权重越高。
- 若用户只问简单定义，`task_type_alignment` 和 `answer_focus` 可提高。
- 权重总和必须为 100。

## 常见失败

- 问原因，只回答上涨事实。
- 问定义，只给指数、行情或查询结果。
- 用户要求核实、截止、重新看，却沿用旧数据。
- 用户要求比较或区别，却只分别介绍。
- 用户指定对象，答案覆盖了泛概念但遗漏对象。
