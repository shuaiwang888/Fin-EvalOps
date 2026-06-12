# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

输出形态在第五类 self_judge schema 基础上增加 pairwise 比较层：动态权重、跳过维度、专家案例、双边维度原始分、双边封顶、双边根因、逐维比较、优势/劣势/学习点和链路归因。调用方负责计算加权分和最终分。

## JSON 结构

> 注：以下示例仅展示常驻维度。按需维度 `product_universe_fit`（relevant/supplementary 时启用）和 `recommendation_stability`（relevant/supplementary 时启用）未在示例中展示，实际输出时应按适用性判断一并包含在 `weight_assignment` 和 `dimension_scores` 中。

```json
{
  "schema_version": "kyc-recommendation-suggestions-self-vs-competitor/v1",
  "pairing": {
        "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "runtime_dimensions": {},
  "weight_assignment": {
    "intent_profile_understanding": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "用户要求结合自身情况推荐"},
    "scenario_emotion_recognition": {"dynamic_weight": 10, "applicability": "relevant", "rationale": "用户表达持续亏损和迷茫，需要识别真实处境"},
    "suitability_personalization": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "推荐必须匹配用户风险、期限和资金目标"},
    "evidence_integration": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需要市场和标的证据支撑推荐"},
    "decision_actionability": {"dynamic_weight": 16, "applicability": "relevant", "rationale": "用户需要可执行的买卖和仓位建议"},
    "risk_boundary_control": {"dynamic_weight": 14, "applicability": "relevant", "rationale": "推荐建议必须有风险边界和证伪条件"},
    "composition_credibility": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "表达清晰度影响用户理解"},
    "tool_usage": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "链路需要核验是否主动使用 KYC 数据和合适工具支撑推荐"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "case13_loss_confusion",
      "matched_reason": "用户表达迷茫和亏损感",
      "hard_checks_used": ["不得直接切到短线荐股", "应先识别情绪和风险状态"]
    }
  ],
  "self_evaluation": {
    "dimension_scores": {
      "intent_profile_understanding": {"raw_score": 0, "evidence": []},
      "scenario_emotion_recognition": {"raw_score": 0, "evidence": []},
      "suitability_personalization": {"raw_score": 0, "evidence": []},
      "evidence_integration": {"raw_score": 0, "evidence": []},
      "decision_actionability": {"raw_score": 0, "evidence": []},
      "risk_boundary_control": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "intent_profile_understanding": {"raw_score": 0, "evidence": []},
      "scenario_emotion_recognition": {"raw_score": 0, "evidence": []},
      "suitability_personalization": {"raw_score": 0, "evidence": []},
      "evidence_integration": {"raw_score": 0, "evidence": []},
      "decision_actionability": {"raw_score": 0, "evidence": []},
      "risk_boundary_control": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []}
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "dimension_comparison": {
    "intent_profile_understanding": {
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
      {"stage": "intent | context | evidence | tool | reasoning | composition | safety_or_compliance", "summary": "", "evidence": []}
    ],
    "competitor": [
      {"stage": "intent | context | evidence | tool | reasoning | composition | safety_or_compliance", "summary": "", "evidence": []}
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

- `schema_version`：固定为 `kyc-recommendation-suggestions-self-vs-competitor/v1`。
- `pairing.case_id`：同题配对键。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识，用于回溯原始样本。
- `pairing.self_model_id`：固定为 `"self"`（被评测的自研模型）。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `runtime_dimensions`：记录本次根据线上维度信号或本题关键缺口新增的临时评分维度；没有新增时输出空对象 `{}`。同题双方必须共用同一组临时维度。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致。权重由 Round 1 确定，Round 2 照抄。所有活跃维度权重和必须等于 100。
- `skipped_dimensions`：标记为 `not_applicable` 的维度列表。仅当该维度完全不适用于本题时才加入。
- `matched_golden_cases`：命中的专家案例和使用的 hard checks。未命中可为空数组。
- `self_evaluation` / `competitor_evaluation`：分别是两边的绝对评测结果，结构遵循第五类 KYC 推荐建议 skill 定义的维度、封顶和根因体系。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，包括适用的按需维度和临时新增维度。每个维度只输出 `raw_score` 和 `evidence`。
- `raw_score`：六档分数，只能取 `0/20/40/60/80/100`。
- `caps`：包含所有触发的封顶规则；若无触发可为空数组。也可包含已检查但未触发的重要规则。
- `root_causes`：按重要程度排列。若所有活跃维度 `raw_score >= 60` 且无封顶触发，可为空数组；否则至少一个。
- `root_causes[*].l1`：必须来自 `intent/context/evidence/tool/reasoning/composition/safety_or_compliance`。
- `root_causes[*].confidence`：`high/medium/low`。
- 若主要问题是没有使用 KYC，`root_causes[*].summary` 必须明确包含“应使用用户 KYC 数据但未使用”或同义说明，便于归因聚合。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据。`score_delta = self_raw_score - competitor_raw_score`。必须覆盖全部活跃维度、按需维度和临时新增维度。
- `self_strengths`：只写自研真正成立的优势；若只是“比竞品稍好但仍未达标”，应优先放入 `shared_failures` 或 `self_weaknesses`。
- `self_weaknesses`：写自研相对竞品或相对专家标准的真实不足。
- `competitor_strengths`：写竞品真正值得学习的地方，必须有答案、上下文、KYC 或链路证据。
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
  "source": "question | self_final_answer | competitor_final_answer | self_context | competitor_context | self_user_profile | competitor_user_profile | self_reasoning | competitor_reasoning | self_function_call | competitor_function_call | self_function_call_output | competitor_function_call_output",
  "pointer": "question | self_record.text_answer | competitor_record.answer | self_record.context[0].answer | self_record.meta.user_investment_goal | competitor_record.chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

## 证据使用原则

- 评分主锚点仍是双方各自最终答案；上下文和 KYC 信息用于理解题目约束、个人化处境和画像要求。
- KYC 画像相关评分必须检查最终答案是否体现用户 KYC 数据，也必须检查链路中是否主动读取、调用、检索或引用用户 KYC 数据。
- 工具调用证据统一从 `self_record.chain[N].tools[M]` / `competitor_record.chain[N].tools[M]` 读取。
- `tool_usage`、根因归因和比较解释允许引用各自链路。
- 当竞品 `plan` 为空时，不要臆造不可见推理；可直接引用工具调用、工具输出和最终答案。
- 输出优势/劣势时，优先用短证据摘要，不要复制长段原文。
- 若一条差异无法追溯到答案、上下文、KYC 或链路证据，不要写成确定结论。
- 不要因为隐藏链路中出现好判断而给最终答案加分；链路只用于解释和 `tool_usage` 评分。

## 序列化规则

- 不要输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`，这些由调用方代码计算。
- JSON 优先，叙事简短。
- 若评分依据不足，必须在 evidence 或 root cause 中体现低置信，而不是编造证据。
