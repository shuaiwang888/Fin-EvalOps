# L1: `context`

用于归因模型没有正确获取或使用用户 KYC 信息。这里的 KYC 信息不限于历史 `context`，也包括画像工具、画像存储、当前问题自述或链路中可见的画像检索结果。

常见 L2：
- `missing-kyc-usage`：05 类推荐建议问题理当使用用户 KYC 数据，但链路和最终答案都没有体现 KYC 使用。
- `missing-kyc-retrieval`：链路没有主动读取、调用或检索用户 KYC 数据，导致后续推荐只能按通用问题处理。
- `ignored-history-profile`：`context` 中已有风险偏好、投资期限、持仓或风格，但最终答案没有使用。
- `ignored-loss-or-holding-context`：上下文已有亏损、成本、持仓，答案按新买入处理。
- `profile-over-inference`：从有限历史过度推断用户画像。
- `context-conflict-not-resolved`：上下文信息冲突，模型没有澄清或条件化处理。

证据要求：
- 引用 `question` 说明本题属于应使用 KYC 的 05 类推荐建议场景。
- 引用 `chain` 中缺少画像读取/调用/检索的表现，或引用已有画像来源未被使用的表现。
- 引用 `text_answer` 中变成通用推荐、未说明画像依据、未体现用户适配的表现。
