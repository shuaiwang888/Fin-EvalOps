# 根因归因体系

| L1 | 链路阶段 | 核心问题 | 文件 |
|---|---|---|---|
| `intent` | 理解问题 | 是否识别真实语义、对象和任务 | [intent.md](intent.md) |
| `evidence` | 检索信息 | 信息是否覆盖正确口径、实体和时点 | [evidence.md](evidence.md) |
| `tool` | 选择与执行工具 | 工具是否选对、实体是否消歧 | [tool.md](tool.md) |
| `reasoning` | 金融语义推理 | 是否把概念、规则和数据口径推对 | [reasoning.md](reasoning.md) |
| `composition` | 组织答案 | 是否把定义、边界、证据和结论讲清楚 | [composition.md](composition.md) |

## 选择规则

- 优先选择最低 raw score 对应维度的根因。
- 若触发封顶规则，优先选择封顶规则对应的根因。
- 每个根因必须绑定证据；证据不足时 `confidence` 用 `low`。
- 合格答案（所有活跃维度 raw score >= 60 且无封顶）可返回空 `root_causes`。
