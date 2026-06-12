"""
10-financial-common-sense-and-semantic-understanding 评测规则定义 (v5)。

金融常识与语义理解类问题：评估模型在金融术语、实体边界、指标口径和语义匹配方面的表现。
"""

DIMENSIONS = [
    {
        "key": "semantic_intent_alignment", "label_zh": "语义意图匹配",
        "description": "评估是否读懂用户真实对象、真实任务和隐含语义。始终考察。",
        "six_level_anchors": {
            0: "完全答非所问，对象或任务核心理解错误",
            20: "仅识别到部分关键词，遗漏真实意图和隐含任务",
            40: "大致方向正确但关键语义偏差，用户需自行补全",
            60: "基本理解用户语义，但个别金融概念或隐含任务未到位",
            80: "准确理解用户语义和隐含任务，仅有极轻微边界不足",
            100: "完美理解用户真实对象、任务和金融语义，无任何偏差",
        },
    },
    {
        "key": "financial_term_understanding", "label_zh": "金融术语/规则理解",
        "description": "评估对金融术语、交易规则、市场黑话和财务概念的理解是否正确。",
        "six_level_anchors": {
            0: "核心金融术语或交易规则完全理解错误",
            20: "关键术语概念出现实质性错误，或混淆基本规则",
            40: "术语理解大致可接受但有明显偏差或定义不准确",
            60: "关键术语理解正确，但个别规则或黑话解释不够精确",
            80: "术语和规则理解准确，解释清晰，仅有极轻微不足",
            100: "金融术语、规则和黑话理解完美，解释精准且可复核",
        },
    },
    {
        "key": "entity_product_boundary", "label_zh": "实体与产品边界",
        "description": "评估是否区分同名公司、股票/基金/ETF/指数/现货、旗下产品等实体边界。",
        "six_level_anchors": {
            0: "将用户对象完全答成另一个实体或产品",
            20: "实体或产品类型出现严重影响结论的混淆",
            40: "大致方向正确但实体边界或产品类型有明显偏差",
            60: "实体和产品识别基本正确，但个别边界说明不够清晰",
            80: "实体和产品边界清晰，区分准确，仅有极轻微遗漏",
            100: "实体与产品边界完美，所有同名公司、品种、上下级产品区分到位",
        },
    },
    {
        "key": "metric_caliber_accuracy", "label_zh": "指标公式与数据口径",
        "description": "评估对PE、ROE、主力控盘、ST、披露期、盘中价格等指标口径的处理是否准确。",
        "six_level_anchors": {
            0: "指标口径完全错误或使用失真数据不做说明",
            20: "关键指标口径出现实质性错误，严重误导结论",
            40: "指标口径大致可接受但存在明显缺失或定义不清晰",
            60: "关键指标口径正确，但个别筛选条件或定义说明不够完整",
            80: "指标口径准确，定义清晰，数据筛选合理",
            100: "指标口径完美准确，所有筛选条件、定义和数据来源均可复核",
        },
    },
    {
        "key": "timeliness_context", "label_zh": "时效上下文",
        "description": "评估是否正确处理最新、近期、当下、盘中、报告期等时间要求。",
        "six_level_anchors": {
            0: "完全忽略时间要求，使用明显过时数据",
            20: "关键时间要求遗漏，使用数据与用户时间语境严重不匹配",
            40: "时间方向大致正确但细节偏差较大，或部分时间要求被忽略",
            60: "时效处理基本正确，但个别数据时点或报告期说明不够精确",
            80: "时效处理准确，数据时点匹配用户需求，仅有极轻微不足",
            100: "时间语境完美匹配，所有数据时点、报告期和最新状态明确标注",
        },
    },
    {
        "key": "credibility_expression", "label_zh": "可信解释与表达",
        "description": "评估答案是否结构清楚、解释到位、避免空泛模板化。",
        "six_level_anchors": {
            0: "输出完全无法阅读或严重不符合问答场景",
            20: "表达混乱，空泛模板化，用户难以判断答案立场",
            40: "有基本结构但解释不足或套用固定模板",
            60: "可读但重点不够突出，部分解释可进一步精确",
            80: "结构清晰，解释到位，措辞审慎，仅有轻微冗余",
            100: "表达完美，先结论后依据，关键信息突出，无模板化套话",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估工具选择、调用参数和链路效率。始终考察。",
        "six_level_anchors": {
            0: "工具完全未使用而应该使用，或每次调用都产生了错误结果",
            20: "工具选择明显错误，或关键步骤本该使用工具但未使用",
            40: "工具选择基本合理但调用参数有误或遗漏了必要的交叉验证",
            60: "工具使用合理但效率不高，或有个别冗余调用",
            80: "工具选择精准，调用高效，交叉验证到位",
            100: "工具使用完美，最小化调用次数达到最大信息覆盖，参数精确",
        },
    },
]

DEFAULT_WEIGHTS = {
    "semantic_intent_alignment": 20,
    "financial_term_understanding": 20,
    "entity_product_boundary": 15,
    "metric_caliber_accuracy": 15,
    "timeliness_context": 10,
    "credibility_expression": 10,
    "tool_usage": 10,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_concept_or_rule_error", "label_zh": "金融概念或规则硬错",
        "label_tag": "金融概念/规则硬错", "severity": "critical", "ceiling": 40,
        "description": "金融概念或交易规则硬错，如集合竞价成交时点、财报披露期、ST状态、PE负值处理。",
    },
    {
        "name": "wrong_entity_or_product", "label_zh": "实体或产品错误",
        "label_tag": "实体/产品错误", "severity": "critical", "ceiling": 45,
        "description": "把用户对象答成另一个实体或产品，如豪威集团/豪能股份、实物黄金/黄金ETF。",
    },
    {
        "name": "missed_core_definition", "label_zh": "遗漏核心定义",
        "label_tag": "遗漏核心定义", "severity": "critical", "ceiling": 55,
        "description": "用户问定义、含义、区别，却主要给行情、指数或数据表。",
    },
    {
        "name": "metric_caliber_unexplained_or_invalid", "label_zh": "指标口径未解释或无效",
        "label_tag": "指标口径未解释/无效", "severity": "warning", "ceiling": 60,
        "description": "使用自定义或失真指标但不解释口径，或指标筛选与投资常识相悖。",
    },
    {
        "name": "stale_or_wrong_time_context", "label_zh": "时效错误或过时",
        "label_tag": "时效错误/过时", "severity": "critical", "ceiling": 60,
        "description": "忽略近期、最新、盘中、报告期等时间要求。",
    },
    {
        "name": "empty_generic_advice", "label_zh": "空泛通用建议",
        "label_tag": "空泛通用建议", "severity": "warning", "ceiling": 65,
        "description": "答案是泛泛建议，缺少与该金融语义场景绑定的解释、案例或数据。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否识别用户的真实金融语义、对象和隐含任务", "l2": ["semantic_target_misread", "financial_term_misunderstood", "entity_product_confusion", "missing_implicit_task"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "获取的数据是否正确、完整、口径匹配", "l2": ["missing_required_data", "wrong_caliber_or_field", "outdated_data", "insufficient_cross_validation"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否选对工具、写对参数、用足链路", "l2": ["wrong_tool_selection", "insufficient_tool_chain", "tool_param_error"]},
    {"l1": "reasoning", "l1_zh": "金融语义推理", "description": "术语解释、实体判断、口径推理是否正确", "l2": ["concept_definition_error", "entity_boundary_error", "metric_caliber_error", "missing_semantic_connection"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "答案是否清晰呈现金融解释和判断", "l2": ["empty_generic_response", "unclear_structure", "missing_definition_or_example"]},
]

ROOT_CAUSE_DIM_MAP = {
    "semantic_intent_alignment": "intent",
    "financial_term_understanding": "reasoning",
    "entity_product_boundary": "reasoning",
    "metric_caliber_accuracy": "evidence",
    "timeliness_context": "evidence",
    "credibility_expression": "composition",
    "tool_usage": "tool",
}

CONFIDENCE_THRESHOLD = 3
