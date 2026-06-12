# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

## JSON 结构

```json
{
  "schema_version": "financial-performance-interpretation-self-vs-competitor/v1",
  "pairing": {
    "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "weight_assignment": {
    "intent_understanding": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "用户要求解释业绩变化和利好利空"},
    "report_data_accuracy": {"dynamic_weight": 15, "applicability": "relevant", "rationale": "需要核验报告期、同比环比和财务口径"},
    "primary_evidence_quality": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "核心原因可能来自年报、季报或公告全文披露"},
    "causal_attribution_depth": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "用户需要解释业绩变化原因"},
    "business_financial_linkage": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需把科目变化连接到业务、行业、成本或会计事件"},
    "forward_investment_judgment": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户询问利好利空、持续性或股价影响"},
    "composition_credibility": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达质量始终有参考价值"},
    "tool_usage": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "两边都提供完整链路，可比较公告全文、财务查询和交叉验证策略"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [],
  "self_evaluation": {
    "dimension_scores": {
      "intent_understanding": {"raw_score": 0, "evidence": []},
      "report_data_accuracy": {"raw_score": 0, "evidence": []},
      "primary_evidence_quality": {"raw_score": 0, "evidence": []},
      "causal_attribution_depth": {"raw_score": 0, "evidence": []},
      "business_financial_linkage": {"raw_score": 0, "evidence": []},
      "forward_investment_judgment": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "intent_understanding": {"raw_score": 0, "evidence": []},
      "report_data_accuracy": {"raw_score": 0, "evidence": []},
      "primary_evidence_quality": {"raw_score": 0, "evidence": []},
      "causal_attribution_depth": {"raw_score": 0, "evidence": []},
      "business_financial_linkage": {"raw_score": 0, "evidence": []},
      "forward_investment_judgment": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "dimension_comparison": {
    "intent_understanding": {
      "winner": "self | competitor | tie",
      "self_raw_score": 0,
      "competitor_raw_score": 0,
      "score_delta": 0,
      "rationale": "",
      "evidence": []
    }
  },
  "self_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "self_weaknesses": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "competitor_strengths": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "shared_failures": [
    {"dimension": "", "summary": "", "evidence": []}
  ],
  "chain_attribution": {
    "self": [
      {"stage": "intent | evidence | tool | reasoning | composition", "summary": "", "evidence": []}
    ],
    "competitor": [
      {"stage": "intent | evidence | tool | reasoning | composition", "summary": "", "evidence": []}
    ],
    "cross_model_observations": []
  },
  "comparison_summary": {
    "absolute_summary": "",
    "relative_summary": "",
    "verdict": "self_better | competitor_better | tie | both_poor",
    "why": []
  }
}
```

## 字段规则

- `schema_version`：固定为 `financial-performance-interpretation-self-vs-competitor/v1`。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识，用于回溯原始样本。
- `pairing.self_model_id`：固定为 `"self"`（被评测的自研模型）。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致。权重由 Round 1 确定，Round 2 照抄；所有 `dynamic_weight` 之和必须 = 100。
- `skipped_dimensions`：标记为 `not_applicable` 的维度列表。这些维度不出现在两边的 `dimension_scores` 和 `dimension_comparison` 中。
- `matched_golden_cases`：命中的专家案例 ID 列表。当用户问题与 golden_cases 中的案例模式匹配时填入；不命中时留空。
- `self_evaluation` / `competitor_evaluation`：分别是两边的绝对评测结果，结构遵循本 skill 定义的维度、封顶和根因体系。
- `dimension_scores`：仅包含活跃维度。每个维度只输出 `raw_score`（严格取 0/20/40/60/80/100 之一）和 `evidence`；不要输出 `weighted_points`、`absolute_score_pre_cap` 或 `final_score`。
- `caps`：包含所有触发的封顶规则，或所有与活跃维度相关且被显式检查过的封顶规则。每条含 `rule_id`、`triggered`、`score_ceiling`、`reason`、`evidence`。
- `root_causes`：有序数组，按重要程度排列。仅在全部活跃维度 `raw_score >= 60` 且无封顶触发时允许返回空数组。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据。`score_delta = self_raw_score - competitor_raw_score`。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品真正值得学习的地方，必须有答案或链路证据。
- `shared_failures`：双方都未达到专家标准时必须填写。
- `chain_attribution`：解释链路如何导致最终答案更好/更差；不要脱离答案单独评价链路“是否漂亮”。
- `comparison_summary.absolute_summary`：先写双方按专家标准各自好不好。
- `comparison_summary.relative_summary`：再写双方谁相对更好。
- `comparison_summary.verdict`：若双方都明显不达标，即便一方分数略高，也应使用 `both_poor`。

## 最终答案锚点

- 自研模型最终答案：优先 `self_record.text_answer`；
- 竞品模型最终答案：若 `competitor_record.text_answer` 为空，则使用 `competitor_record.answer`；
- 若编排层已生成统一字段，可读取归一化字段，但证据仍需回指原始字段。

## 证据对象格式

```json
{
  "source": "question | self_final_answer | competitor_final_answer | self_context | competitor_context | self_reasoning | competitor_reasoning | self_function_call | competitor_function_call | self_function_call_output | competitor_function_call_output",
  "pointer": "question | self_record.text_answer | competitor_record.answer | self_record.chain[0].plan | competitor_record.chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

## 证据使用原则

- 评分主锚点仍是双方各自最终答案。
- 工具调用证据统一从 `self_record.chain[N].tools[M]` / `competitor_record.chain[N].tools[M]` 读取。
- `tool_usage`、根因归因和比较解释允许引用各自链路。
- 当竞品 `plan` 为空时，不要臆造不可见推理；可直接引用工具调用、工具输出和最终答案。
- 输出优势/劣势时，优先用短证据摘要，不要复制长段原文。
- 若一条差异无法追溯到答案或链路证据，不要写成确定结论。

## 叙事评审模板

- `absolute_summary`：先说明双方按专家标准各自是否合格。
- `relative_summary`：再说明自研相对竞品领先/落后在哪里。
- `why`：仅列真正驱动结论的高信号原因。
