# 根因归因索引

根因用于解释复杂选股答案为什么降分。先看触发的封顶规则，再看最低分活跃维度。

| L1 | 文件 | 适用问题 |
|---|---|---|
| `intent` | [intent.md](intent.md) | 长问句条件、否定条件、隐性指令、输出要求遗漏 |
| `semantics` | [semantics.md](semantics.md) | 金融指标、交易语义、业务口径、数据频率误解 |
| `planning` | [planning.md](planning.md) | 未分层筛选、前后关系丢失、跨领域交集未处理 |
| `tool` | [tool.md](tool.md) | 工具选择、关键词、参数、交叉验证或读取输出错误 |
| `data_logic` | [data_logic.md](data_logic.md) | 日期、交易日、分时、公式、不可用数据边界错误 |
| `result` | [result.md](result.md) | 候选池、排序、字段、无结果说明不满足要求 |
| `composition` | [composition.md](composition.md) | 表达混乱、数据堆砌、表格图表无决策价值 |

## 归因规则

1. 若触发封顶规则，优先把主要根因归到封顶违规维度。
2. 否则按活跃维度 raw_score 升序、dynamic_weight 降序选择主要根因。
3. 每个根因必须绑定证据，证据可来自 `question`、`text_answer`、`chain.plan`、工具调用、工具输出或专家批注。
4. summary 必须写清机制，例如“把北向资金日频流入当作可用条件，导致筛选计划建立在已停更口径上”。
