# `evidence` — 检索数据

当工具选对了、用对了，但获取到的数据本身有问题时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `wrong-data-value` | 数据值错误：取错字段（如营业成本取成其他科目）、用错复权方式、日期对应错位。注意：基础数据取错导致衍生计算失效，根因仍归本 L2（数据层面错误），不归 reasoning/formula-error | data_retrieval_accuracy |
| `data-depth-insufficient` | 数据深度不足：长期历史数据不完整（如"上市以来"仅找到最近一年），统计样本量不足 | data_retrieval_accuracy |
| `data-completeness-gap` | 数据覆盖不全：遗漏符合条件的标的、遗漏用户要求的指标、部分年份数据缺失 | data_retrieval_accuracy, intent_fulfillment |
