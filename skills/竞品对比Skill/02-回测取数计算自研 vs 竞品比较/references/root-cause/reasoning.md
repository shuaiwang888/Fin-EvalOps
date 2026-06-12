# `reasoning` — 计算与推理

当计算逻辑、推理过程或拆解步骤出错时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `formula-error` | 财务公式选择错误：毛利率/费用率等公式用错、复权方式选择错误（未复权 vs 前复权）、概率定义错误 | calculation_accuracy |
| `arithmetic-error` | 算术运算错误：加减乘除计算失误、求和/平均值计算错误、百分比换算出错 | calculation_accuracy |
| `decomposition-failure` | 多步逻辑拆解失败：无法将复合条件分解为可执行的子步骤，跳步或简化关键条件 | logical_decomposition |
| `time-reasoning-error` | 时间推理错误：日历日与交易日推算错误、节假日倒推失误、时间范围计算偏差 | time_inference |
