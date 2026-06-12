# 根因归因索引

根因用于解释分数下降发生在哪里。先按触发的封顶规则和最低分活跃维度确定主要根因，再选择最贴近机制的 L1/L2。

| L1 | 文件 | 适用问题 |
|---|---|---|
| `intent` | [intent.md](intent.md) | 未正确拆解复合意图、时间窗口、对象或输出要求 |
| `coverage` | [coverage.md](coverage.md) | 子任务漏答、主次错位、展开不足 |
| `evidence` | [evidence.md](evidence.md) | 多源证据浅、错、无关或没有整合 |
| `tool` | [tool.md](tool.md) | 工具选择、输入、读取或编排问题 |
| `data_logic` | [data_logic.md](data_logic.md) | 计算口径、时间窗口、案例真实性、推演自洽性问题 |
| `reasoning` | [reasoning.md](reasoning.md) | 事实到影响、传导、策略没有闭环 |
| `composition` | [composition.md](composition.md) | 结构混乱、信息拼盘、表格杂、结论不凝练 |
| `latency` | [latency.md](latency.md) | 耗时过长且质量收益不足 |

## 归因规则

1. 先看触发的封顶规则。若某个封顶规则上限较低，优先把主要根因归到触发该封顶的维度。
2. 再看活跃维度 raw_score，按分数升序、动态权重降序排序。
3. 每个根因必须绑定证据，证据可来自 `question`、`context`、`text_answer`、`chain.plan`、工具调用、工具输出或耗时证据。
4. 根因 summary 必须写清机制，例如“漏掉利润贡献和估值两个子任务，使产业链需求判断无法转化为公司受益排序”。
