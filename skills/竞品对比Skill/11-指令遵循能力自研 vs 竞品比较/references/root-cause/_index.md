# 根因归因体系

| L1 | 链路阶段 | 核心问题 | 文件 |
|---|---|---|---|
| `intent` | 指令识别 | 是否抽取出用户主指令和约束 | [intent.md](intent.md) |
| `evidence` | 证据收集 | 证据是否服务主指令 | [evidence.md](evidence.md) |
| `tool` | 工具执行 | 工具是否为完成指令而用 | [tool.md](tool.md) |
| `reasoning` | 指令转换 | 是否把数据转成用户要求的答案类型 | [reasoning.md](reasoning.md) |
| `composition` | 答案呈现 | 主答案是否放在前面且聚焦 | [composition.md](composition.md) |

优先选择触发封顶规则或最低 raw score 的维度作为主根因。
