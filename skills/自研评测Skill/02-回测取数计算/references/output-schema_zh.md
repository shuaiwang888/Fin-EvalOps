# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短的自然语言评审。

## JSON 结构

```json
{
  "schema_version": "backtesting/v4",
  "weight_assignment": {
    "intent_fulfillment": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "用户要求完整盈亏计算"},
    "data_retrieval_accuracy": {"dynamic_weight": 25, "applicability": "relevant", "rationale": "核心取数任务"},
    "time_inference": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "涉及具体日期开盘价和收盘价"},
    "calculation_accuracy": {"dynamic_weight": 20, "applicability": "relevant", "rationale": "核心计算任务"},
    "logical_decomposition": {"dynamic_weight": 0, "applicability": "not_applicable", "rationale": "单步取数计算，无需多步拆解"},
    "result_verifiability": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "单次计算，明细有助于验证"},
    "expression_quality": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达质量有参考价值"},
    "tool_usage": {"dynamic_weight": 5, "applicability": "relevant", "rationale": "需评估工具选择"},
    "latency_efficiency": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "简单任务，耗时影响有限"}
  },
  "skipped_dimensions": ["logical_decomposition"],
  "matched_golden_cases": [
    {
      "case_id": "case10",
      "matched": true,
      "hard_checks_used": ["必须使用2026-03-10开盘价和2026-03-25收盘价", "一手A股按100股计算"]
    }
  ],
  "dimension_scores": {
    "intent_fulfillment": {"raw_score": 0, "evidence": []},
    "data_retrieval_accuracy": {"raw_score": 0, "evidence": []},
    "time_inference": {"raw_score": 0, "evidence": []},
    "calculation_accuracy": {"raw_score": 0, "evidence": []},
    "result_verifiability": {"raw_score": 0, "evidence": []},
    "expression_quality": {"raw_score": 0, "evidence": []},
    "tool_usage": {"raw_score": 0, "evidence": []},
    "latency_efficiency": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "data_fabrication",
      "triggered": true,
      "score_ceiling": 35,
      "reason": "答案编造了涨停后高开概率统计数据，实际样本量和概率值均无法验证。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "reasoning",
      "l2": "time-reasoning-error",
      "dimension": "time_inference",
      "raw_score": 1,
      "confidence": "high",
      "summary": "将交易日幻觉为非交易日，导致后续计算的锚定日期错误。",
      "evidence": []
    }
  ],
  "narrative_review": {
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "next_actions": []
  }
}
```

> **注意**：`weighted_points`、`absolute_score_pre_cap`、`final_score` 由调用方代码自动计算，你不需要输出这些字段。`dimension_scores` 中每个维度只需输出 `raw_score` 和 `evidence`。`root_causes` 中不需要输出 `dynamic_weight`。

## 证据对象格式

使用紧凑的证据条目：

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output | timing",
  "pointer": "context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

指针格式对应输入数据结构：

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案的纯文本版本（评分主锚点） |
| `context` | `context[N].answer` | 对话中第 N 轮的历史答案 |
| `reasoning` | `chain[N].plan` | 第 N 步的规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用（含 name + input） |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具调用的输出 |
| `timing` | `timing.total_seconds \| chain[N].elapsed_seconds` | 总响应耗时或单步耗时 |

评分时以 `text_answer` 为主锚点。仅在评估呈现或可视化质量时引用 `answer`（markdown 版本）。

除非调用方明确要求，不要输出长引文。

## 字段规则

- `schema_version`：`backtesting/v4`。v4 将算术计算（`weighted_points`、`absolute_score_pre_cap`、`final_score`）移至调用方代码，LLM 只负责判断和打分。
- `weight_assignment`：每个维度的动态权重分配结果。包含 `dynamic_weight`（整数）、`applicability`（`relevant`/`supplementary`/`not_applicable`）、`rationale`（简短理由）。所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表。这些维度不出现在 `dimension_scores` 中。
- `matched_golden_cases`：记录命中的专家案例和实际使用的 hard checks；未命中时允许为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，不含 `skipped_dimensions` 中的维度。每个维度只需输出 `raw_score`（六档：0/20/40/60/80/100）和 `evidence`（证据数组）。`weighted_points`、`dynamic_weight` 由代码自动填充。
- `caps`：包含所有考虑过的封顶规则（仅与活跃维度相关的），或至少包含所有触发的封顶规则
- `root_causes`：有序数组，按重要程度排列。仅从活跃维度中选择根因。仅在合格通过（所有活跃维度 raw_score ≥ 60 且无封顶触发）时允许返回空数组。否则必须返回至少一个根因——算法团队据此认领问题。证据不足时设 `confidence: "low"`。每个元素标识 L1/L2、它解释的维度、以及将 L2 机制与该维度失败模式融合的一句话 summary。`raw_score` 用于可追溯性。`dynamic_weight` 由代码自动填充。
- `root_causes[*].dimension`：该根因所解释的维度——最低分维度，或封顶规则驱动主要根因时的封顶违规维度
- `root_causes[*].raw_score`：该维度的 raw_score，用于可追溯性
- `narrative_review`：保持简短且可执行

## 叙事评审模板

保持可读且简洁：
- `summary`：一段话概括整体判断
- `strengths`：仅列出真正的优势
- `weaknesses`：驱动分数的主要不足
- `next_actions`：产品团队可以执行的修复建议

## 序列化规则

在机器可读性和文字表现力之间选择时，优先保持 JSON 稳定，缩短叙事。
