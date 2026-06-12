"""
10-financial-common-sense-and-semantic-understanding-self-vs-competitor
评测规则定义。

该比较 skill 沿用第 10 类金融常识与语义理解的绝对评分维度、默认权重、
封顶规则和根因体系；pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "semantic_intent_alignment",
        "label_zh": "语义意图匹配",
        "description": "判断是否读懂用户真实对象、真实任务和隐含语义。",
    },
    {
        "key": "financial_term_understanding",
        "label_zh": "金融术语/规则理解",
        "description": "判断是否准确理解金融术语、交易规则、市场黑话和财务概念。",
    },
    {
        "key": "entity_product_boundary",
        "label_zh": "实体与产品边界",
        "description": "判断是否区分同名公司、股票/基金/ETF/指数/现货和旗下产品。",
    },
    {
        "key": "metric_caliber_accuracy",
        "label_zh": "指标公式与数据口径",
        "description": "判断 PE、ROE、主力控盘、ST、披露期、盘中价格等口径是否正确。",
    },
    {
        "key": "timeliness_context",
        "label_zh": "时效上下文",
        "description": "判断是否正确处理最新、近期、当下、盘中、报告期等时间语义。",
    },
    {
        "key": "credibility_expression",
        "label_zh": "可信解释与表达",
        "description": "判断解释是否清楚、可信，是否避免空泛或无证据表达。",
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "判断工具选择、实体消歧、口径核验和证据转化是否合理。",
    },
]

# 默认权重与自研 skill 的建议权重保持一致，sum=100。

DEFAULT_WEIGHTS = {
    "semantic_intent_alignment": 20,
    "financial_term_understanding": 20,
    "entity_product_boundary": 15,
    "metric_caliber_accuracy": 15,
    "timeliness_context": 10,
    "credibility_expression": 10,
    "tool_usage": 10,
}

CAP_RULES = [
    {
        "name": "hard_concept_or_rule_error",
        "label_zh": "金融概念或交易规则硬错",
        "severity": "critical",
        "ceiling": 40,
        "description": "金融概念或交易规则硬错，如集合竞价成交时点、财报披露期、ST 状态、PE 负值处理。",
    },
    {
        "name": "wrong_entity_or_product",
        "label_zh": "实体或产品错配",
        "severity": "critical",
        "ceiling": 45,
        "description": "把用户对象答成另一个实体或产品，如豪威集团/豪能股份、实物黄金/黄金 ETF、基金公司/旗下基金。",
    },
    {
        "name": "missed_core_definition",
        "label_zh": "遗漏核心定义",
        "severity": "critical",
        "ceiling": 55,
        "description": "用户问定义、含义、区别，却主要给行情、指数或数据表。",
    },
    {
        "name": "metric_caliber_unexplained_or_invalid",
        "label_zh": "指标口径未解释或失真",
        "severity": "warning",
        "ceiling": 60,
        "description": "使用自定义或失真指标但不解释口径，或指标筛选与投资常识相悖。",
    },
    {
        "name": "stale_or_wrong_time_context",
        "label_zh": "时效上下文错误",
        "severity": "warning",
        "ceiling": 60,
        "description": "忽略近期、最新、盘中、报告期等时间要求。",
    },
    {
        "name": "empty_generic_advice",
        "label_zh": "泛泛建议",
        "severity": "warning",
        "ceiling": 65,
        "description": "答案是泛泛建议，缺少与该金融语义场景绑定的解释、案例或数据。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "理解问题",
        "description": "是否识别真实语义、对象和任务。",
        "l2": [
            "semantic-target-misread",
            "implicit-meaning-missed",
            "definition-vs-data-confused",
            "time-intent-missed",
        ],
    },
    {
        "l1": "evidence",
        "l1_zh": "检索信息",
        "description": "信息是否覆盖正确口径、实体和时点。",
        "l2": [
            "wrong-entity-evidence",
            "wrong-caliber-evidence",
            "insufficient-definition-evidence",
            "stale-evidence",
        ],
    },
    {
        "l1": "tool",
        "l1_zh": "选择与执行工具",
        "description": "工具是否选对，实体和产品是否正确消歧。",
        "l2": [
            "entity-disambiguation-failed",
            "wrong-tool-for-caliber",
            "tool-output-overtrusted",
            "missing-realtime-check",
        ],
    },
    {
        "l1": "reasoning",
        "l1_zh": "金融语义推理",
        "description": "是否把概念、规则和数据口径推对。",
        "l2": [
            "concept-boundary-broken",
            "market-rule-misread",
            "metric-validity-missed",
            "semantic-correction-missing",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "组织答案",
        "description": "是否把定义、边界、证据和结论讲清楚。",
        "l2": [
            "definition-not-first",
            "caliber-not-explained",
            "generic-advice",
            "ambiguity-not-disclosed",
        ],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "semantic_intent_alignment": "intent",
    "financial_term_understanding": "reasoning",
    "entity_product_boundary": "reasoning",
    "metric_caliber_accuracy": "reasoning",
    "timeliness_context": "evidence",
    "credibility_expression": "composition",
    "tool_usage": "tool",
}
