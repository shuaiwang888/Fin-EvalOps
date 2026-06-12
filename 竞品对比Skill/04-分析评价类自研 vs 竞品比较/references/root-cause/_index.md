# 根因归因体系

L1 分类用于跨评测聚合统计，L2 用于定位可执行问题。根因必须绑定证据。

## 链路阶段

| L1 | 链路阶段 | 核心问题 | 文件 |
|---|---|---|---|
| `intent` | 理解问题 | 是否识别真实投资场景和必备要素 | [intent.md](intent.md) |
| `evidence` | 检索信息 | 找到的信息是否关键、充分、专业、时效正确 | [evidence.md](evidence.md) |
| `tool` | 选择与执行工具 | 是否选对工具、写对输入、用足链路 | [tool.md](tool.md) |
| `reasoning` | 推导投资逻辑 | 是否把信息转成投资判断和因果链 | [reasoning.md](reasoning.md) |
| `composition` | 组织答案 | 最终答案是否把关键逻辑讲清楚 | [composition.md](composition.md) |
| `capability_gap` | 数据源/能力缺口 | 当前工具或数据源缺少必要深层资料 | [capability_gap.md](capability_gap.md) |

## 证据规则

每个根因必须绑定证据。证据可以来自：
- `question`
- `text_answer`
- `context[N].answer`
- `chain[N].plan`
- `chain[N].tools[M]`
- `chain[N].tools[M].output`

如果证据不足但诊断有用，设置 `confidence: "low"`，并保持结论克制。

## 置信度规则

- `high`：最终答案或链路直接支撑
- `medium`：强烈暗示但缺少完整证据
- `low`：合理怀疑，证据不足

## 选择规则

1. 先查看是否触发封顶规则。若封顶上限低，该封顶对应的失败模式优先作为主要根因。
2. 否则按 active 维度 raw_score 升序排列；并列时按动态权重降序，再按维度名排序。
3. 最低分维度映射到最重要根因。
4. 继续扫描低分维度，若有独立病因（不同 L1 或不同 L2）则追加。
5. 返回最多 8 个根因。若所有 active 维度 raw_score >= 60 且无封顶触发，可返回空数组。
6. `summary` 必须写成因果句：因为链路/答案哪里出了问题，所以哪个维度被拉低。

## evidence 与 tool 的边界

- 工具选对了、用法也合理，但信息本身不关键、过时或来源浅 -> `evidence`
- 工具选错、输入错、漏用必要工具或误用工具约束 -> `tool`
- 工具和信息都有，但没有推导成投资逻辑 -> `reasoning`
- 链路里有逻辑，最终答案没讲出来 -> `composition`
- 当前工具体系没有该类专业资料或数据源 -> `capability_gap`
