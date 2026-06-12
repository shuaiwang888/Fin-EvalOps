# 输出格式规范

先输出结构化 JSON。在调用方需要可读摘要时，JSON 后附简短自然语言评审。

输出形态与既有 self_judge schema 保持一致：运行时维度、动态权重、跳过维度、专家案例、维度原始分、封顶、根因、叙事评审。调用方负责计算加权分和最终分。

## JSON 结构

```json
{
  "schema_version": "analysis-evaluation/v1",
  "runtime_dimensions": {
    "business_purity": {
      "definition": "题材或产业链问题中，标的业务与主题的真实相关度是否被准确判断。",
      "why_added": "线上样本显示模型常把弱相关标的当作核心受益标的，现有维度难以单独承载该缺口。",
      "scoring_anchor": "0-5 分，重点看业务收入、订单、客户或产品与主题的直接相关性。"
    }
  },
  "weight_assignment": {
    "intent_scenario_recognition": {
      "dynamic_weight": 12,
      "applicability": "relevant",
      "rationale": "用户询问个股能否买入，核心是识别短期题材驱动、基本面驱动以及真实决策需求。"
    },
    "evidence_source_quality": {
      "dynamic_weight": 12,
      "applicability": "relevant",
      "rationale": "需要依据最新催化、财务和公告等材料支撑判断。"
    },
    "recency_time_boundary": {
      "dynamic_weight": 8,
      "applicability": "relevant",
      "rationale": "问题涉及当前行情和近期题材发酵。"
    },
    "investment_logic_depth": {
      "dynamic_weight": 18,
      "applicability": "relevant",
      "rationale": "需要判断核心投资逻辑是否成立。"
    },
    "method_fit": {
      "dynamic_weight": 11,
      "applicability": "relevant",
      "rationale": "分析方法必须匹配标的属性和投资周期。"
    },
    "comparison_quantification": {
      "dynamic_weight": 5,
      "applicability": "supplementary",
      "rationale": "可用对比和量化增强判断，但不是本题主矛盾。"
    },
    "actionability_risk": {
      "dynamic_weight": 8,
      "applicability": "relevant",
      "rationale": "用户需要可执行的买卖或观察条件。"
    },
    "user_profile_suitability": {
      "dynamic_weight": 7,
      "applicability": "relevant",
      "rationale": "用户要求个人化持仓/买卖建议，推荐必须受风险偏好、持仓成本和期限约束。"
    },
    "scenario_emotion_recognition": {
      "dynamic_weight": 4,
      "applicability": "supplementary",
      "rationale": "用户存在亏损或焦虑信号，答案需要避免诱导高风险短线操作。"
    },
    "composition_credibility": {
      "dynamic_weight": 3,
      "applicability": "supplementary",
      "rationale": "表达影响可信度。"
    },
    "tool_usage": {
      "dynamic_weight": 5,
      "applicability": "relevant",
      "rationale": "需要检查链路是否使用合适工具支撑分析。"
    },
    "business_purity": {
      "dynamic_weight": 7,
      "applicability": "relevant",
      "rationale": "用户关心题材是否真能支撑标的上涨，业务纯度直接影响投资结论。"
    }
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
    "business_purity": {"raw_score": 0, "evidence": []}
  },
  "caps": [
    {
      "rule_id": "missed_core_investment_logic",
      "triggered": true,
      "score_ceiling": 60,
      "reason": "题材股问题未分析题材发酵、级别、空间和持续性。",
      "evidence": []
    }
  ],
  "root_causes": [
    {
      "l1": "reasoning",
      "l2": "no-theme-fermentation-logic",
      "dimension": "investment_logic_depth",
      "raw_score": 1,
      "confidence": "high",
      "summary": "答案用技术面和财务指标替代题材发酵逻辑，导致用户最关心的空间和持续性没有被解释。",
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

## 证据对象格式

```json
{
  "source": "question | final_answer | context | reasoning | function_call | function_call_output",
  "pointer": "question | text_answer | context[0].answer | chain[0].plan | chain[0].tools[0] | chain[0].tools[0].output",
  "summary": "简短证据摘要"
}
```

| source | pointer 格式 | 指向 |
|---|---|---|
| `question` | `question` | 用户当前问题 |
| `final_answer` | `text_answer` | 最终答案纯文本 |
| `context` | `context[N].answer` | 第 N 轮历史答案 |
| `reasoning` | `chain[N].plan` | 第 N 步规划/推理文本 |
| `function_call` | `chain[N].tools[M]` | 第 N 步第 M 次工具调用 |
| `function_call_output` | `chain[N].tools[M].output` | 第 N 步第 M 次工具输出 |

不要输出长引文；证据摘要应短而具体。

## 字段规则

- `schema_version`：固定为 `analysis-evaluation/v1`。
- `runtime_dimensions`：记录本次根据线上维度信号或本题关键缺口新增的维度；没有新增时输出空对象 `{}`。
- `weight_assignment`：包含全部活跃维度和本次明确跳过的种子维度。每个维度有 `dynamic_weight`、`applicability`、`rationale`。所有活跃维度权重和必须等于 100。
- `skipped_dimensions`：`not_applicable` 维度名称列表；可只包含本次曾检查但决定跳过的种子维度。
- `matched_golden_cases`：命中的专家案例和使用的 hard checks。未命中可为空数组。
- `dimension_scores`：仅包含 `relevant` 和 `supplementary` 维度，包括适用的运行时维度。每个维度只输出 `raw_score` 和 `evidence`。
- `caps`：包含所有触发的封顶规则；若无触发可为空数组。也可包含已检查但未触发的重要规则。
- `root_causes`：按重要程度排列。若所有活跃维度 raw_score >= 60 且无封顶触发，可为空数组；否则至少一个。
- `root_causes[*].l1`：必须来自 `intent/evidence/tool/reasoning/composition/capability_gap`。
- `root_causes[*].confidence`：`high/medium/low`。
- `narrative_review`：保持简短，重点写可执行改进建议。

## 序列化规则

- 不要输出 `weighted_points`、`absolute_score_pre_cap`、`final_score`，这些由调用方代码计算。
- JSON 优先，叙事简短。
- 若评分依据不足，必须在 evidence 或 root cause 中体现低置信，而不是编造证据。
