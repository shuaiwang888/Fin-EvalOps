# `intent` — 指令识别

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `primary-instruction-missed` | 未识别用户主指令 | explicit_instruction_completion |
| `task-type-misread` | 把原因、定义、比较、排序等任务类型读错 | task_type_alignment |
| `constraint-missed` | 漏掉时间、对象、范围或排除条件 | constraint_coverage |
| `secondary-info-overweighted` | 把辅助信息当成主问 | answer_focus |
