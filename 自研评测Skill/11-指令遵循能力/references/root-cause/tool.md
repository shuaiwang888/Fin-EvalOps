# `tool` — 工具执行

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `tool-query-not-aligned` | 工具查询没有围绕主指令设计 | tool_usage, explicit_instruction_completion |
| `tool-result-not-transformed` | 工具只返回数据，模型没有转化为原因/定义/比较 | task_type_alignment, tool_usage |
| `missing-required-tool-check` | 需要时点核实但未调用合适工具 | constraint_coverage, tool_usage |
| `over-fetching` | 过度取数导致答案焦点漂移 | answer_focus, tool_usage |
