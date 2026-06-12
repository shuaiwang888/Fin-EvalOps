"""
10-financial-common-sense-and-semantic-understanding result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义金融常识与语义理解领域的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "semantic_intent_alignment",
        "label_zh": "语义意图匹配",
        "description": "评估最终回答是否读懂用户真实对象、真实任务、错别字、黑话和隐含语义。",
        "six_level_anchors": {
            0: "完全未识别用户真实意图，答案与问题无关或直接跑偏",
            20: "只抓住表层关键词，遗漏用户核心对象或真实任务",
            40: "部分理解意图，但错别字、黑话、隐含对象或任务边界有明显偏差",
            60: "基本理解用户意图，但个别语义约束或对象范围不够精准",
            80: "准确理解真实意图、对象和关键约束，仅有轻微可改进处",
            100: "完美理解所有显性和隐性语义，能正确纠偏并处理不确定性",
        },
    },
    {
        "key": "financial_term_understanding",
        "label_zh": "金融术语/规则理解",
        "description": "评估最终回答是否准确解释金融术语、交易规则、市场黑话和财务概念。",
        "six_level_anchors": {
            0: "核心金融概念或交易规则完全错误",
            20: "只做泛泛科普，术语含义、规则或市场语境严重缺失",
            40: "理解了部分术语，但关键规则、常见误区或场景含义存在明显问题",
            60: "术语和规则解释基本正确，但边界、例外或适用条件不够清楚",
            80: "术语、规则和市场语境解释准确，常见误区处理较好",
            100: "概念、规则、例外和市场语义解释完美，专业且可验证",
        },
    },
    {
        "key": "entity_product_boundary",
        "label_zh": "实体与产品边界",
        "description": "评估最终回答是否区分同名公司、近名公司、股票/基金/ETF/指数/现货和旗下产品。",
        "six_level_anchors": {
            0: "实体或产品完全错配，导致答案对象错误",
            20: "严重混淆公司、代码、基金、ETF、指数或现货等对象",
            40: "识别了大致对象，但关键边界或相似实体仍有明显混用",
            60: "实体和产品边界基本正确，但对歧义、旗下产品或代码关系说明不足",
            80: "实体和产品边界清晰，能处理相似名称和口径差异",
            100: "对象识别完美，所有实体、产品、代码和上下级关系均准确无误",
        },
    },
    {
        "key": "metric_caliber_accuracy",
        "label_zh": "指标公式与数据口径",
        "description": "评估最终回答中 PE、ROE、主力控盘、ST、披露期、盘中价格等指标和口径是否正确。",
        "six_level_anchors": {
            0: "关键指标公式、数据口径或规则时点完全错误",
            20: "指标解释严重失真，未说明公式、适用边界或常见陷阱",
            40: "部分口径正确，但负值处理、报告期、盘中时点或自定义指标存在明显问题",
            60: "主要口径正确，但公式、来源、局限或异常值处理不够清楚",
            80: "指标口径准确，公式、时点和适用边界解释到位",
            100: "指标口径完美，公式、报告期、异常值、局限和投资含义均处理精准",
        },
    },
    {
        "key": "timeliness_context",
        "label_zh": "时效上下文",
        "description": "评估最终回答是否正确处理最新、近期、当下、盘中、报告期等时间语义。",
        "six_level_anchors": {
            0: "完全无视时间要求，使用错误时点导致结论不可用",
            20: "时间语义严重误读，最新、近期、盘中或报告期处理明显错误",
            40: "有时间意识但关键时间窗口、披露节奏或数据时点存在偏差",
            60: "时间上下文基本正确，但个别日期、报告期或时点说明不够精确",
            80: "时效处理准确，能匹配问题中的时间边界并说明限制",
            100: "时效上下文完美，所有日期、时点、报告期和可用性边界均清楚",
        },
    },
    {
        "key": "credibility_expression",
        "label_zh": "可信解释与表达",
        "description": "评估最终回答是否清楚、可信、审慎，是否避免空泛建议和不可验证断言。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导、编造或无法阅读",
            20: "表达空泛混乱，大量主观断言或模板化建议",
            40: "有部分可信内容，但结构、证据或语气存在明显问题",
            60: "表达基本清楚可信，但部分断言缺少支撑或结论不够突出",
            80: "结构清晰、措辞审慎，证据和结论匹配良好",
            100: "表达完美，定义、边界、证据、结论和风险提示均清楚可信",
        },
    },
]

# 默认权重（总和 100），LLM 动态权重回退时使用。
# 原过程相关权重已分散到可从最终回答判断的答案质量维度。

DEFAULT_WEIGHTS = {
    "semantic_intent_alignment": 22,
    "financial_term_understanding": 22,
    "entity_product_boundary": 17,
    "metric_caliber_accuracy": 17,
    "timeliness_context": 11,
    "credibility_expression": 11,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_concept_or_rule_error",
        "label_zh": "金融概念或交易规则硬错",
        "label_tag": "金融概念/交易规则硬错",
        "severity": "critical",
        "ceiling": 40,
        "score_effect": "tag_only",
        "description": "最终回答中的金融概念或交易规则出现实质错误，如集合竞价成交时点、财报披露期、ST 状态、PE 负值处理。",
    },
    {
        "name": "wrong_entity_or_product",
        "label_zh": "实体或产品错配",
        "label_tag": "实体/产品错配",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答把用户对象答成另一个实体或产品，如豪威集团/豪能股份、实物黄金/黄金 ETF、基金公司/旗下基金。",
    },
    {
        "name": "missed_core_definition",
        "label_zh": "遗漏核心定义",
        "label_tag": "遗漏核心定义",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "用户询问定义、含义、区别或规则，最终回答却主要给行情、指数、列表或数据表。",
    },
    {
        "name": "metric_caliber_unexplained_or_invalid",
        "label_zh": "指标口径未解释或失真",
        "label_tag": "指标口径未解释/失真",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答使用自定义或失真指标但不解释口径，或指标筛选与基础投资常识相悖。",
    },
    {
        "name": "stale_or_wrong_time_context",
        "label_zh": "时效上下文错误",
        "label_tag": "时效上下文错误",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答忽略近期、最新、盘中、报告期等时间要求，或使用错误时点支撑结论。",
    },
    {
        "name": "empty_generic_advice",
        "label_zh": "泛泛建议",
        "label_tag": "泛泛建议",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "最终回答是泛泛建议，缺少与该金融语义场景绑定的定义、证据、案例或数据。",
    },
]

ALLOWED_EVIDENCE_SOURCES = {
    "question",
    "self_final_answer",
    "competitor_final_answer",
}

ALLOWED_EVIDENCE_POINTERS = {
    "question",
    "self_record.text_answer",
    "self_record.answer",
    "competitor_record.text_answer",
    "competitor_record.answer",
    "normalized.self_final_answer",
    "normalized.competitor_final_answer",
}
