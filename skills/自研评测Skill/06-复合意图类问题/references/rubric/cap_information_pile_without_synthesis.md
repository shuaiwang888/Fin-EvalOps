# 封顶规则：`information_pile_without_synthesis`

## 触发条件

最终答案收集或罗列大量新闻、公告、行业、财务或行情信息，但没有形成统一判断和“事实—影响—传导—策略”闭环。

典型表现：
- 信息拼盘，新闻与核心标的关联弱
- 多源信息没有解释如何影响市场、行业、公司或策略
- 表格和资料很多，但用户无法得出结论
- 只写“可能利好/可能利空”，没有传导路径和条件

## 分数上限

`score_ceiling = 60`

## 不触发条件

- 答案先罗列信息，但随后明确归纳影响、传导路径和策略。
- 信息源本身错误、浅层或不匹配（应由 `wrong_or_shallow_evidence_mix` 覆盖）。

## 与 `wrong_or_shallow_evidence_mix` 的边界

本规则聚焦"信息量充足但缺乏综合判断"，即信息拼盘问题；`wrong_or_shallow_evidence_mix` 聚焦"信息源本身质量不足"，即证据基础问题。若两者同时存在，按更严重者封顶，不叠加。

## 关联维度

- `multi_source_evidence_integration`
- `analysis_chain_closure`
- `composition_readability`
