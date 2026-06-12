# `composition` — 组织答案

当逻辑可能正确但答案未能充分呈现时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `detail-omission` | 关键明细遗漏：仅输出结论而缺少逐行数据明细、日期列表、每个数据点的值 | result_verifiability |
| `process-hidden` | 推理过程隐藏：计算步骤不透明，公式代入过程未展示，用户无法复现或校验。归因边界：缺失明细导致用户无法验证归 `result_verifiability`；排版混乱导致可读性差归 `expression_quality` | result_verifiability, expression_quality |
| `format-degradation` | 格式退化：缺乏结构化展示（无表格、无汇总），数据堆砌无可读性 | expression_quality, intent_fulfillment |
