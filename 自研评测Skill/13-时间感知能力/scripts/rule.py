"""
13-time-awareness-ability 评测规则定义 (v5)。

时间感知能力类问题：评估模型在时间锚点解析、交易日历判断、数据时点核验和财报期映射方面的表现。
"""

DIMENSIONS = [
    {
        "key": "temporal_intent_recognition", "label_zh": "时间意图识别",
        "description": "评估是否识别用户问题中的显式/隐式时间意图。",
        "six_level_anchors": {
            0: "完全忽略时间词，按普通行情/分析题处理",
            20: "仅识别到部分时间线索但遗漏关键时间语义",
            40: "识别到时间相关但遗漏关键锚点或未区分自然日/交易日",
            60: "基本识别时间意图但个别时间词解析不够精确",
            80: "准确抽取时间词、市场/标的、自然日/交易日/报告期语义",
            100: "完美识别所有显式和隐式时间意图，包括跨市场时区和交易日差异",
        },
    },
    {
        "key": "anchor_date_resolution", "label_zh": "锚点日期解析",
        "description": "评估相对时间是否正确解析为绝对日期、星期和年份。",
        "six_level_anchors": {
            0: "把相对时间解析到完全错误的日期或年份",
            20: "关键日期解析错误，如周几算错、年份映射错误",
            40: "大体正确但缺少时区、星期或绝对日期说明",
            60: "日期解析基本正确但个别细节可优化",
            80: "基于请求时间和时区正确解析，答案中呈现必要日期",
            100: "日期解析完美精确，所有相对时间均映射到正确的绝对日期/时间戳",
        },
    },
    {
        "key": "market_calendar_status", "label_zh": "交易日历状态",
        "description": "评估是否判断对应市场在目标日期是否交易。",
        "six_level_anchors": {
            0: "休市日仍给出当日交易结论",
            20: "交易日历判断严重错误，张冠李戴不同市场日历",
            40: "知道可能涉及交易日历但仅泛泛提示，未落实到目标日期/市场",
            60: "交易日历判断基本正确但跨市场差异说明不足",
            80: "正确判断目标市场交易状态，区分休市、半日市、盘中/盘后",
            100: "交易日历完美判断，所有市场状态、交易时段和跨市场差异均正确",
        },
    },
    {
        "key": "data_asof_freshness", "label_zh": "数据时点新鲜度",
        "description": "评估是否核验数据日期，防止旧数据冒充当前事实。",
        "six_level_anchors": {
            0: "把旧数据当成今天/最新事实，没有任何提示",
            20: "数据明显过时但答案未做任何说明",
            40: "使用的数据大致可接受但as-of说明不足",
            60: "数据时点基本正确但as-of标注不够完整",
            80: "明确数据as-of，若无最新数据说明原因",
            100: "所有数据时点精确标注，as-of透明，替代数据使用有充分理由",
        },
    },
    {
        "key": "period_disclosure_mapping", "label_zh": "财报期间映射",
        "description": "评估财报、分红、报告期和披露期的映射是否正确。",
        "six_level_anchors": {
            0: "把披露日/分红日/报告期混为一谈，或私自替换年份",
            20: "报告期或披露期映射出现严重影响结论的错误",
            40: "报告期方向正确但披露期或替代口径说明不完整",
            60: "报告期映射基本正确但个别边界说明可优化",
            80: "区分自然语言年份、财政/报告期、披露日期和最新可得数据",
            100: "财报、分红、报告期和披露期映射完美，所有年份和期间边界清晰",
        },
    },
    {
        "key": "premise_correction_clarification", "label_zh": "前提纠错与澄清",
        "description": "评估发现用户时间前提错误时是否主动纠错。",
        "six_level_anchors": {
            0: "完全不纠错，顺着错误前提生成看似完整的错误答案",
            20: "有提示但不充分，用户仍可能采信错误前提",
            40: "有部分提示但放在后文或没有充分阻止误解",
            60: "基本完成纠错但表达可更直接清晰",
            80: "开头直接澄清错误前提，并给可用替代问法或可回答口径",
            100: "纠错完美，清晰否定错误前提，给出准确替代方案，确保用户不被误导",
        },
    },
    {
        "key": "answer_composition_credibility", "label_zh": "答案可信表达",
        "description": "评估最终答案是否让用户清楚理解时间口径和可信边界。",
        "six_level_anchors": {
            0: "模板化套话掩盖关键时间错误",
            20: "表达混乱，时间边界模糊或容易误解",
            40: "主结论可读但时间边界散乱或不够突出",
            60: "表达基本清晰但时间口径和限制可更明确",
            80: "日期、市场、数据时点、限制和替代口径表达清楚",
            100: "时间口径和可信边界完美呈现，用户一眼可判断数据适用范围",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估链路是否正确使用工具核验时间、交易日历和数据时点。",
        "six_level_anchors": {
            0: "应查交易日历/行情日期却没查，或查了错误市场/日期",
            20: "工具选择明显错误，关键时间核验步骤缺失",
            40: "工具方向正确但输入或读取不完整",
            60: "工具使用合理但效率不高或有个别遗漏",
            80: "调用合适工具，输入包含正确市场/代码/日期/报告期，正确读取返回日期",
            100: "工具使用完美，所有时间相关核验完整，输入参数精确，输出解读正确",
        },
    },
]

DEFAULT_WEIGHTS = {
    "temporal_intent_recognition": 15,
    "anchor_date_resolution": 15,
    "market_calendar_status": 15,
    "data_asof_freshness": 15,
    "period_disclosure_mapping": 10,
    "premise_correction_clarification": 10,
    "answer_composition_credibility": 10,
    "tool_usage": 10,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "hard_wrong_anchor_date", "label_zh": "硬性锚点日期错误",
        "label_tag": "硬性锚点日期错误", "severity": "critical", "ceiling": 40,
        "description": "核心相对日期、星期或年份解析错误，且该错误影响主结论。",
    },
    {
        "name": "market_closed_answered_as_open", "label_zh": "休市按交易作答",
        "label_tag": "休市按交易作答", "severity": "critical", "ceiling": 35,
        "description": "目标市场/品种在目标日期无交易，答案仍给出当日涨跌、开盘走势或交易结论，且未说明休市。",
    },
    {
        "name": "stale_data_masquerading_as_today", "label_zh": "旧数据冒充当前",
        "label_tag": "旧数据冒充当前", "severity": "critical", "ceiling": 45,
        "description": "用旧行情、旧价格、旧公告或旧财报回答今天/最新问题，且最终答案未显式说明as-of。",
    },
    {
        "name": "missing_required_premise_correction", "label_zh": "缺失必要前提纠错",
        "label_tag": "缺失必要前提纠错", "severity": "critical", "ceiling": 50,
        "description": "用户问题的时间前提明显错误或不可成立，答案未先纠错，导致用户可能采信错误前提。",
    },
    {
        "name": "fiscal_period_disclosure_error", "label_zh": "财报期间披露错误",
        "label_tag": "财报期间披露错误", "severity": "critical", "ceiling": 50,
        "description": "财报/分红/报告期映射错误，尤其把自然语言年份、报告期、披露日、分红实施日混淆。",
    },
    {
        "name": "fabricated_time_fact", "label_zh": "编造时间事实",
        "label_tag": "编造时间事实", "severity": "critical", "ceiling": 30,
        "description": "编造市场是否开盘、节假日、星期、数据日期、公告日期或报告期事实。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否识别用户问题中的时间意图和锚点需求", "l2": ["missed_temporal_intent", "wrong_relative_time_anchor", "ambiguous_time_not_clarified", "wrong_market_entity"]},
    {"l1": "evidence", "l1_zh": "检索数据", "description": "获取的时间数据是否正确、完整", "l2": ["no_calendar_evidence", "stale_data_not_detected", "report_period_evidence_mismatch", "insufficient_asof_evidence"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否使用正确工具核验时间信息", "l2": ["calendar_tool_missing", "wrong_tool_date_input", "tool_output_date_misread", "fallback_without_disclosure"]},
    {"l1": "reasoning", "l1_zh": "时间逻辑推理", "description": "时间推理是否正确", "l2": ["natural_day_trading_day_confusion", "fiscal_year_calendar_year_confusion", "premise_not_rejected", "date_weekday_inconsistency", "template_overrides_time_check"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "答案是否清晰呈现时间口径", "l2": ["asof_not_visible", "correction_buried", "misleading_current_tense"]},
    {"l1": "capability_gap", "l1_zh": "能力边界", "description": "工具或数据源的覆盖限制", "l2": ["market_calendar_coverage_gap", "disclosure_data_coverage_gap"]},
]

ROOT_CAUSE_DIM_MAP = {
    "temporal_intent_recognition": "intent",
    "anchor_date_resolution": "intent",
    "market_calendar_status": "reasoning",
    "data_asof_freshness": "evidence",
    "period_disclosure_mapping": "evidence",
    "premise_correction_clarification": "reasoning",
    "answer_composition_credibility": "composition",
    "tool_usage": "tool",
}

CONFIDENCE_THRESHOLD = 3
