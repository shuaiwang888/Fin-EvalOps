# 根因归因索引

根因用于解释分数下降发生在哪里。先按最低分活跃维度和触发的封顶规则确定主要根因，再选择最贴近机制的 L1/L2。

| L1 | 文件 | 适用问题 |
|---|---|---|
| `intent` | [intent.md](intent.md) | 误解推荐任务、未识别“适合我”、未区分买卖/持有/配置 |
| `context` | [context.md](context.md) | 没有使用用户 KYC 数据、历史提问、持仓、偏好、风格，或错误使用上下文 |
| `evidence` | [evidence.md](evidence.md) | 关键数据缺失、证据浅、证据与推荐不匹配 |
| `tool` | [tool.md](tool.md) | 工具选择、输入、输出读取或效率问题 |
| `reasoning` | [reasoning.md](reasoning.md) | 推荐逻辑、适当性、仓位、触发条件推理失败 |
| `composition` | [composition.md](composition.md) | 模板化、啰嗦、主结论不清、表达可信度差 |
| `safety_or_compliance` | [safety_or_compliance.md](safety_or_compliance.md) | 过度确定、风险边界缺失、不适当高风险推荐 |

## 归因规则

1. 先看触发的封顶规则。若某个封顶规则上限较低，优先把主要根因归到触发该封顶的维度。
2. 再看活跃维度 raw_score，按分数升序、动态权重降序排序。
3. 每个根因必须绑定证据，证据可来自 `question`、`context`、`text_answer`、`chain.plan`、工具调用或工具输出。
4. 不能只写“答案不够好”。必须写清机制，例如“05 类推荐建议理当使用用户 KYC 数据，但模型未读取或使用画像，导致 ETF 推荐无法证明适配用户风险期限”。
5. 若主要问题是未使用 KYC，根因 summary 必须明确写出“应使用用户 KYC 数据但未使用”或同义表述，方便算法团队聚合认领。
