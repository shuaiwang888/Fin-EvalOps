# 质量标签：`fabricated_user_profile`

## 触发条件

最终回答编造或无依据推断用户画像，并将该画像作为推荐依据，例如：
- 无依据声称用户是稳健型、激进型、短线型、长期型。
- 无依据声称用户资金规模、持仓、成本、风险等级或投资经验。
- 将不确定信息当成确定画像使用。

## 分数上限

`score_ceiling = 55`

## 不触发条件

- 答案明确使用条件化表述，如“如果你偏稳健”“若你能承受较大波动”。
- 用户问题本身已经提供了相应画像或约束，答案只是据此展开。

## 关联维度

- `intent_profile_understanding`
- `suitability_personalization`
- `composition_credibility`
