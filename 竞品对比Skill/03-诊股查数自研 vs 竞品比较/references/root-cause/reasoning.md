# `reasoning` — 计算、口径和金融推理

当基础数据可能存在，但计算、对比、换算或市场框架推理出错时使用。

| L2 | 说明 | 典型受影响维度 |
|---|---|---|
| `calculation-error` | 涨跌幅、总额、差值、跑赢、累计、比价或金额计算错误 | calculation_comparison |
| `time-caliber-reasoning-error` | 时间、交易日、复权、单位、合约、汇率、分红日类型等口径推理错误 | time_caliber_precision |
| `market-framework-mismatch` | 没用市场常用框架，如筹码、主力、增长点、止盈位、商品比价框架错位 | analysis_framework_fit |
| `incremental-vs-stock-confusion` | 把存量优势当增长点，未识别边际变化 | insight_extension, analysis_framework_fit |
| `comparison-not-synthesized` | 多标的/多周期数据没有转化为差异、强弱、排序或结论 | calculation_comparison, insight_extension |
| `causal-chain-incomplete` | 有数据但没有解释传导关系、原因和观察点 | insight_extension, analysis_framework_fit |
