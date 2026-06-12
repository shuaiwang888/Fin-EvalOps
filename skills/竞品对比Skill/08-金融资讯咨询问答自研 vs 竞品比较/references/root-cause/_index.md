# 根因归因索引

根因用于解释为什么最终答案得分下降。只从活跃评分维度中选择根因。

## L1 分类

| L1 | 文件 | 说明 |
|---|---|---|
| `intent` | [intent.md](intent.md) | 问题意图、隐含诉求、子问题理解错误 |
| `evidence` | [evidence.md](evidence.md) | 信息检索、证据来源、时效和事实质量问题 |
| `tool` | [tool.md](tool.md) | 工具选择、参数、执行和交叉验证问题 |
| `reasoning` | [reasoning.md](reasoning.md) | 从资讯到影响、主因、标的的推理问题 |
| `composition` | [composition.md](composition.md) | 答案组织、重点呈现和表达边界问题 |

## 选择规则

1. 按 `raw_score` 升序排列活跃维度；并列时看动态权重，权重高者优先。
2. 若封顶规则触发且比最低分维度更能解释最终分下降，根因绑定封顶违规维度。
3. 根因 evidence 必须来自问题、最终答案、上下文、规划链路、工具调用或工具输出。
4. `confidence` 使用 `high`、`medium`、`low`。证据明确且直接对应低分维度时为 high；只能推测时为 low。
5. 不要把同一个问题拆成多个重复根因；优先给产品/算法团队可执行的根因。

## 维度到 L1 的默认映射

| 维度 | 默认 L1 |
|---|---|
| `intent_fulfillment` | `intent` |
| `timeliness_fact_boundary` | `evidence` |
| `fact_evidence_quality` | `evidence` |
| `information_integration` | `reasoning` |
| `investment_mapping` | `reasoning` |
| `core_signal_extraction` | `reasoning` |
| `nonstandard_source_awareness` | `evidence` |
| `credibility_expression` | `composition` |
| `tool_usage` | `tool` |

