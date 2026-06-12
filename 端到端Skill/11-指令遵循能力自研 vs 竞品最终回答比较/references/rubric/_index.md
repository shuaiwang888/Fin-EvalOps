# 评分细则索引

本 rubric 只评估最终回答文本本身。所有维度的证据只能来自用户问题、自研最终回答或竞品最终回答。

## 维度列表

以下维度在评测时根据题目分析动态分配权重。表中“建议权重”仅作参考基准，实际权重由步骤 1 的题目分析决定。

| 维度 | 建议权重 | 文件 | 适用性判断指南 |
|---|---:|---|---|
| `explicit_instruction_completion` 显式指令完成 | 35 | [explicit_instruction_completion.md](explicit_instruction_completion.md) | **始终 relevant**。主指令是否被完成 |
| `task_type_alignment` 任务类型对齐 | 22 | [task_type_alignment.md](task_type_alignment.md) | **始终 relevant**。原因、定义、比较、排序、建议等任务类型是否对齐 |
| `constraint_coverage` 约束覆盖 | 18 | [constraint_coverage.md](constraint_coverage.md) | **relevant**: 用户有时间、范围、对象、排除条件或格式约束。**supplementary**: 无显式约束但仍需检查对象边界 |
| `answer_focus` 答案焦点 | 15 | [answer_focus.md](answer_focus.md) | **始终 relevant**。是否围绕主问展开，而非数据堆砌或跑题 |
| `necessary_information_completeness` 必要信息完整度 | 10 | [necessary_information_completeness.md](necessary_information_completeness.md) | **relevant**: 主指令需要原因、定义边界、比较标准、核实依据或决策支撑。**supplementary**: 简单直接问答 |

## 动态权重分配规则

1. 仅阅读用户问题，对每个维度判断适用性：`relevant` / `supplementary` / `not_applicable`。
2. 主指令越明确，`explicit_instruction_completion` 权重越高。
3. 用户要求的任务类型越容易被误答，`task_type_alignment` 权重越高。
4. 明确约束越多，`constraint_coverage` 权重越高。
5. 如果题目容易被行情、背景、长列表或模板话术淹没主答案，`answer_focus` 权重应保持较高。
6. 主指令需要原因、定义边界、比较标准、排序依据或核实结论时，提高 `necessary_information_completeness`。
7. 所有动态权重之和必须 = 100。

## Result-only 通用检查项

每个活跃维度都必须能回指最终回答证据，并覆盖下列检查：
- 是否直接满足用户真实意图，而非只给背景、数据、过程描述或泛泛建议。
- 是否给出明确结论、解释、定义、比较、排序、分层或可执行判断。
- 是否存在事实、时间、实体、数值、口径、定义或边界错误。
- 是否覆盖用户要求的关键子问题、对象范围、比较维度和必要步骤。
- 结论与理由是否闭合，是否有跳步、偷换概念或因果断裂。
- 关键断言是否有证据支撑，是否可验证。
- 是否避免把涨跌幅、成交额、指数、表格或查询结果替代用户真正要求的答案。

## 常见失败

- 问原因，只回答上涨事实。
- 问定义，只给指数、行情或查询结果。
- 用户要求核实、截止、重新看，却没有体现时点。
- 用户要求比较或区别，却只分别介绍。
- 用户指定对象，答案覆盖了泛概念但遗漏对象。
- 用户要求建议或选择，答案只罗列信息，没有给判断标准和结论。

## 封顶标签

- [primary_instruction_missing（参考上限 45）](cap_primary_instruction_missing.md)
- [wrong_task_type（参考上限 50）](cap_wrong_task_type.md)
- [critical_constraint_ignored（参考上限 60）](cap_critical_constraint_ignored.md)
- [data_dump_without_instruction_answer（参考上限 55）](cap_data_dump_without_instruction_answer.md)
- [answer_focus_drift（参考上限 65）](cap_answer_focus_drift.md)

## 封顶标签注意事项

- 本类别沿用原规则语义：封顶规则作为质量标签记录在 `applied_caps`，不直接修改 `final_score`。
- 封顶标签不替代维度评分；触发标签后仍需完成逐维评分。
- 封顶标签只能依据最终回答文本触发。
