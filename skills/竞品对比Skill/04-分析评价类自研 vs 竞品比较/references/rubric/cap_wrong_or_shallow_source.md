# 封顶规则：`wrong_or_shallow_source`

分数上限：`55`

当答案使用了错误证据类型，或题目需要专业深层来源但答案只用浅层公开搜索并给出确定结论时触发。

触发条件：
- 用通用行业材料替代调研纪要、研报全文、公告或数据库证据
- 客户占比、供应链绑定、订单份额等深层资料问题，未说明来源限制却强行回答
- 用研报或旧专题冒充近期新闻事件
- 关键来源缺失导致结论不可验证

不触发条件：
- 答案明确说明来源不足，并给出合理的下一步验证路径。

根因优先映射：
- `evidence.wrong-evidence-type`
- `evidence.source-depth-insufficient`
- `capability_gap.missing-specialized-source`
