# 专家案例基准

## case_01 赛马概念领涨海南橡胶上涨原因分析
Query: 截止今天上午 9 点 36 分赛马概念领涨，海南橡胶也涨，的原因。
hard checks:
- 主指令是“分析原因”，必须解释赛马概念领涨和海南橡胶上涨的驱动因素。
- 涨幅、成交、板块表现只能作为证据，不等同于原因。
- 若答案只写“赛马概念涨幅明显、海南橡胶同步上涨”，触发 `primary_instruction_missing` 或 `data_dump_without_instruction_answer`。
- 合格答案应至少覆盖政策/事件催化、板块情绪、个股关联和时点信息中的关键项。

主要维度：`explicit_instruction_completion`, `task_type_alignment`, `answer_focus`

## case_02 什么是微盘股它的流通市值是多少
Query: 什么是微盘股，它的流通市值是多少？
hard checks:
- 主指令是解释“什么是微盘股”，应先给定义和常见口径。
- 流通市值是辅助信息，不能用“微盘股指数流通市值查询结果”替代定义。
- 若答案只给日期、流通市值、涨跌幅，触发 `wrong_task_type`。

主要维度：`explicit_instruction_completion`, `task_type_alignment`, `necessary_information_completeness`

## 跨案例锚点

- “原因”题必须从事实走向因果解释。
- “定义”题必须从概念边界开始。
- “区别/比较”题必须直接对比差异，不能分别百科。
- “怎么选/建议”题必须给决策标准和结论，不能只列信息。
- “截止/当下/重新核实”题必须体现时点。
