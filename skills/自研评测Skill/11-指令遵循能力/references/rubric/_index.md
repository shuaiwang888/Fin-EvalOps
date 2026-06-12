# 评分细则索引

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中"建议权重"仅作参考基准，实际权重由步骤 0 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---|---|---|
| `explicit_instruction_completion` 显式指令完成 | 30 | [explicit_instruction_completion.md](explicit_instruction_completion.md) | **始终 relevant**。主指令是否被完成 |
| `task_type_alignment` 任务类型对齐 | 20 | [task_type_alignment.md](task_type_alignment.md) | **始终 relevant**。原因、定义、比较、排序、建议等任务类型是否对齐 |
| `constraint_coverage` 约束覆盖 | 15 | [constraint_coverage.md](constraint_coverage.md) | 用户有时间、范围、对象、排除条件时 relevant；否则 supplementary |
| `answer_focus` 答案焦点 | 15 | [answer_focus.md](answer_focus.md) | **始终 relevant**。是否围绕主问展开，而非数据堆砌或跑题 |
| `necessary_information_completeness` 必要信息完整度 | 10 | [necessary_information_completeness.md](necessary_information_completeness.md) | 主指令需要证据链时 relevant；否则 supplementary |
| `tool_usage` 工具使用合理性 | 10 | [tool_usage.md](tool_usage.md) | **始终 relevant** |

## 动态权重分配规则

1. 先抽取 `primary_instruction`，再评估答案。
2. 主指令越明确，`explicit_instruction_completion` 权重越高。
3. 明确约束越多，`constraint_coverage` 权重越高。
4. 若用户只问简单定义，`task_type_alignment` 和 `answer_focus` 可提高。
5. 权重总和必须为 100。

## 封顶规则

- [primary_instruction_missing（上限 45）](cap_primary_instruction_missing.md)
- [wrong_task_type（上限 50）](cap_wrong_task_type.md)
- [critical_constraint_ignored（上限 60）](cap_critical_constraint_ignored.md)
- [data_dump_without_instruction_answer（上限 55）](cap_data_dump_without_instruction_answer.md)
- [answer_focus_drift（上限 65）](cap_answer_focus_drift.md)

## 封顶规则注意事项

- 封顶限制最终分数，不替代维度评分。
- 若多条同时触发，取最低上限。

## 常见失败

- 问原因，只回答上涨事实。
- 问定义，只给指数、行情或查询结果。
- 用户要求核实、截止、重新看，却沿用旧数据。
- 用户要求比较或区别，却只分别介绍。
- 用户指定对象，答案覆盖了泛概念但遗漏对象。
