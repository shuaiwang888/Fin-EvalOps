# 质量标签：`overconfident_or_unsuitable_recommendation`

## 触发条件

最终回答给出过度确定或明显不适当的投资建议，可能误导用户承担不匹配的风险，例如：
- 使用确定性收益、确定性底部、必涨、稳赚、一定反弹等表达。
- 对高风险、短线、主题或单一行业推荐没有仓位和适用人群边界。
- 对明显低风险或亏损用户推荐高波动集中仓位。
- 对加仓、抄底、追涨给出强建议但没有证伪条件。
- 对普通“适合我”ETF/基金推荐默认给窄行业或高波动主题，并暗示适合长期持有，但没有画像和组合边界支撑。

## 分数上限

`score_ceiling = 55`

## 不触发条件

- 答案给出明确但条件化的建议，并充分说明风险、仓位和证伪条件。

## 关联维度

- `risk_boundary_control`
- `suitability_personalization`
- `composition_credibility`
