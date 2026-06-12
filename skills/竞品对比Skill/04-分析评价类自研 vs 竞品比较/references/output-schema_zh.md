# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

输出形态在第四类 self_judge schema 基础上增加 pairwise 比较层：运行时维度、动态权重、跳过维度、专家案例、双边维度原始分、双边封顶、双边根因、逐维比较、优势/劣势/学习点和链路归因。调用方负责计算加权分和最终分。

## JSON 结构

```json
{
  "schema_version": "analysis-evaluation-self-vs-competitor/v1",
  "pairing": {
        "case_id": "",
    "self_model_id": "self",
    "competitor_model_id": "",
    "same_question_verified": true
  },
  "runtime_dimensions": {
    "business_purity": {
      "definition": "题材或产业链问题中，标的业务与主题的真实相关度是否被准确判断。",
      "why_added": "线上样本显示模型常把弱相关标的当作核心受益标的，现有维度难以单独承载该缺口。",
      "scoring_anchor": "0/20/40/60/80/100 六档分，重点看业务收入、订单、客户或产品与主题的直接相关性。"
    }
  },
  "weight_assignment": {
    "intent_scenario_recognition": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "用户询问个股能否买入，核心是识别短期题材驱动、基本面驱动以及真实决策需求。"},
    "evidence_source_quality": {"dynamic_weight": 12, "applicability": "relevant", "rationale": "需要依据最新催化、财务和公告等材料支撑判断。"},
    "recency_time_boundary": {"dynamic_weight": 8, "applicability": "relevant", "rationale": "问题涉及当前行情和近期题材发酵。"},
    "investment_logic_depth": {"dynamic_weight": 18, "applicability": "relevant", "rationale": "需要判断核心投资逻辑是否成立。"},
    "method_fit": {"dynamic_weight": 11, "applicability": "relevant", "rationale": "分析方法必须匹配标的属性和投资周期。"},
    "comparison_quantification": {"dynamic_weight": 5, "applicability": "supplementary", "rationale": "可用对比和量化增强判断，但不是本题主矛盾。"},
    "actionability_risk": {"dynamic_weight": 8, "applicability": "relevant", "rationale": "用户需要可执行的买卖或观察条件。"},
    "user_profile_suitability": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "用户要求个人化持仓/买卖建议，推荐必须受风险偏好、持仓成本和期限约束。"},
    "scenario_emotion_recognition": {"dynamic_weight": 4, "applicability": "supplementary", "rationale": "用户存在亏损或焦虑信号，答案需要避免诱导高风险短线操作。"},
    "composition_credibility": {"dynamic_weight": 3, "applicability": "supplementary", "rationale": "表达影响可信度。"},
    "tool_usage": {"dynamic_weight": 5, "applicability": "relevant", "rationale": "两边都提供完整链路，可比较工具使用策略。"},
    "business_purity": {"dynamic_weight": 7, "applicability": "relevant", "rationale": "用户关心题材是否真能支撑标的上涨，业务纯度直接影响投资结论。"}
  },
  "skipped_dimensions": [],
  "matched_golden_cases": [
    {
      "case_id": "Case 6",
      "case_name": "典型题材股现在能不能买",
      "used_hard_checks": [
        "必须围绕题材回答：题材是什么、什么时候发酵、逻辑有多大、能否持续、还有多大空间。"
      ]
    }
  ],
  "self_evaluation": {
    "dimension_scores": {
      "intent_scenario_recognition": {"raw_score": 0, "evidence": []},
      "evidence_source_quality": {"raw_score": 0, "evidence": []},
      "recency_time_boundary": {"raw_score": 0, "evidence": []},
      "investment_logic_depth": {"raw_score": 0, "evidence": []},
      "method_fit": {"raw_score": 0, "evidence": []},
      "comparison_quantification": {"raw_score": 0, "evidence": []},
      "actionability_risk": {"raw_score": 0, "evidence": []},
      "user_profile_suitability": {"raw_score": 0, "evidence": []},
      "scenario_emotion_recognition": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []},
      "business_purity": {"raw_score": 0, "evidence": []}  // 运行时维度，仅当 runtime_dimensions 中定义了 business_purity 时才输出
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "competitor_evaluation": {
    "dimension_scores": {
      "intent_scenario_recognition": {"raw_score": 0, "evidence": []},
      "evidence_source_quality": {"raw_score": 0, "evidence": []},
      "recency_time_boundary": {"raw_score": 0, "evidence": []},
      "investment_logic_depth": {"raw_score": 0, "evidence": []},
      "method_fit": {"raw_score": 0, "evidence": []},
      "comparison_quantification": {"raw_score": 0, "evidence": []},
      "actionability_risk": {"raw_score": 0, "evidence": []},
      "user_profile_suitability": {"raw_score": 0, "evidence": []},
      "scenario_emotion_recognition": {"raw_score": 0, "evidence": []},
      "composition_credibility": {"raw_score": 0, "evidence": []},
      "tool_usage": {"raw_score": 0, "evidence": []},
      "business_purity": {"raw_score": 0, "evidence": []}  // 运行时维度，仅当 runtime_dimensions 中定义了 business_purity 时才输出
    },
    "caps": [],
    "root_causes": [],
    "narrative_review": {"summary": "", "strengths": [], "weaknesses": [], "next_actions": []}
  },
  "dimension_comparison": {
    "intent_scenario_recognition": {
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
      {"stage": "intent | evidence | tool | reasoning | composition | capability_gap", "summary": "", "evidence": []}
    ],
    "competitor": [
      {"stage": "intent | evidence | tool | reasoning | composition | capability_gap", "summary": "", "evidence": []}
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

- `schema_version`：固定为 `analysis-evaluation-self-vs-competitor/v1`。
- `pairing.case_id`：同题配对键。
- `pairing.case_id`：同题配对键，自研与竞品共享的唯一标识，用于回溯原始样本。
- `pairing.self_model_id`：固定为 `"self"`（被评测的自研模型）。
- `pairing.competitor_model_id`：竞品模型名称，取自输入数据。
- `pairing.same_question_verified`：若为 `false`，不得继续输出胜负结论。
- `runtime_dimensions`：记录本次根据线上维度信号或本题关键缺口新增的维度；没有新增时输出空对象 `{}`。同题双方必须共用同一组运行时维度。
- `weight_assignment`：同一题下双方共享的动态权重，必须完全一致。权重由 Round 1 确定，Round 2 照抄。所有活跃维度权重和必须等于 100。
- `skipped_dimensions`：标记为 `not_applicable` 的维度列表。仅当该维度完全不适用于本题时才加入。
- `matched_golden_cases`：命中的专家案例和使用的 hard checks。未命中可为空数组。
- `self_evaluation` / `competitor_evaluation`：分别是两边的绝对评测结果，结构遵循本 skill 定义的维度、封顶和根因体系。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，包括适用的运行时维度。每个维度只输出 `raw_score` 和 `evidence`。
- `caps`：包含所有触发的封顶规则；若无触发可为空数组。也可包含已检查但未触发的重要规则。
- `root_causes`：按重要程度排列。若所有活跃维度 raw_score >= 60 且无封顶触发，可为空数组；否则至少一个。
- `root_causes[*].l1`：必须来自 `intent/evidence/tool/reasoning/composition/capability_gap`。
- `root_causes[*].confidence`：`high/medium/low`。
- `dimension_comparison`：逐维输出谁更强、分差、理由和证据。`score_delta = self_raw_score - competitor_raw_score`。必须覆盖全部活跃维度和运行时维度。
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
  "pointer": "question | self_record.text_answer | competitor_record.answer | self_record.context[0].answer | self_record.chain[0].plan | competitor_record.chain[0].tools[0].output",
  "summary": "简短的证据摘要"
}
```

## 证据使用原则

- 评分主锚点仍是双方各自最终答案；上下文只用于理解题目约束、个人化处境和画像要求。
- 工具调用证据统一从 `self_record.chain[N].tools[M]` / `competitor_record.chain[N].tools[M]` 读取。
- `tool_usage`、根因归因和比较解释允许引用各自链路。
- 当竞品 `plan` 为空时，不要臆造不可见推理；可直接引用工具调用、工具输出和最终答案。
- 输出优势/劣势时，优先用短证据摘要，不要复制长段原文。
- 若一条差异无法追溯到答案或链路证据，不要写成确定结论。

## 序列化规则

- 不要输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`，这些由调用方代码计算。
- JSON 优先，叙事简短。
- 若评分依据不足，必须在 evidence 或 root cause 中体现低置信，而不是编造证据。
