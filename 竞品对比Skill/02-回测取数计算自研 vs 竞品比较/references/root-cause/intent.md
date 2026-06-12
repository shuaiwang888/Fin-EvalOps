# `intent` — 理解问题

当系统误解了用户的取数计算需求时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `calculation-type-misread` | 误解计算类型：将概率计算理解为排序，将回测理解为选股，将盈亏计算理解为行情查询 | intent_fulfillment |
| `subtask-missed` | 遗漏用户的子任务：如只提取数据未计算衍生指标，或只计算未与历史对比，或漏掉部分指标 | intent_fulfillment, logical_decomposition |
| `scope-constraint-missed` | 忽略时间范围、标的范围、阈值条件等用户指定的约束 | intent_fulfillment, data_retrieval_accuracy |
