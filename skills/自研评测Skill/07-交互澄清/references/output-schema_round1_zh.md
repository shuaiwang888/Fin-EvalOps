# Round 1 输出格式

用于只做盲评、暂不做完整根因归因的轻量输出。若调用方要求完整 self_judge，使用 [output-schema_zh.md](output-schema_zh.md)。

```json
{
  "schema_version": "interactive-clarification/round1/v1",
  "weight_assignment": {},
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "dimension_scores": {},
  "round1_notes": {
    "major_quality_risks": [],
    "requires_chain_review": ["tool_usage"],
    "requires_context_review": []
  }
}
```

规则：
- `dimension_scores` 只输出活跃维度的 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`。
- `tool_usage`、`latency_efficiency`、完整 `root_causes` 可在第二阶段补齐。
- 如果发现硬性交易规则错误、实体错配或多轮承接断裂，必须在 `round1_notes.major_quality_risks` 中写明。
