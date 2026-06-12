# 封顶规则

| rule_id | 上限 | 触发条件 |
|---|---:|---|
| `primary_instruction_missing` | 45 | 用户主指令未完成，例如问原因但无原因 |
| `wrong_task_type` | 50 | 答案任务类型错误，例如问定义却答指数查询 |
| `critical_constraint_ignored` | 60 | 忽略关键时间、对象、范围或排除条件 |
| `data_dump_without_instruction_answer` | 55 | 大量数据堆砌但未回答主问 |
| `answer_focus_drift` | 65 | 有部分相关内容，但重点明显偏离用户要求 |

若多条同时触发，取最低上限。
