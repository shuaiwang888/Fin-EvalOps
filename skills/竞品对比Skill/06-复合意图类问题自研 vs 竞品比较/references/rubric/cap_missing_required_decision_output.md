# 封顶规则：`missing_required_decision_output`

## 触发条件

用户明确要求投资结论、策略、择股、布局、调仓、合约、价位、正套做法或利润测算，但最终答案没有给出可执行输出。

典型表现：
- 只讲研究背景，不回答“是否应布局或调仓”
- 只讲热点板块，不给择股流程或核心股票
- 只讲品种逻辑，不回答做哪个合约、价位和盈亏
- 情景推演没有上破/下破触发标准或应对策略

## 分数上限

`score_ceiling = 65`

## 不触发条件

- 答案因证据不足不直接给确定结论，但给出清晰条件、观察点和下一步验证路径。

## 关联维度

- `decision_actionability`
- `analysis_chain_closure`
- `task_coverage_priority`
