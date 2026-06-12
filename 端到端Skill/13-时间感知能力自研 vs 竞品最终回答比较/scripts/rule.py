"""
13-time-awareness-ability result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义时间感知领域的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "temporal_intent_recognition",
        "label_zh": "时间意图识别",
        "description": "评估最终回答是否识别用户问题中的显式/隐式时间意图。",
        "six_level_anchors": {
            0: "完全按普通行情/分析题处理，忽略时间词",
            20: "严重忽略核心时间词，仅有少量无关正确内容",
            40: "识别到部分时间线索，但关键锚点明显遗漏",
            60: "识别到时间相关，但遗漏关键锚点或没有区分自然日/交易日",
            80: "基本准确抽取时间词和主要锚点，仅有轻微边界缺口",
            100: "准确抽取时间词、市场/标的、自然日/交易日/报告期语义，并说明需要的锚点",
        },
    },
    {
        "key": "anchor_date_resolution",
        "label_zh": "锚定日期解析",
        "description": "评估最终回答是否把相对时间解析到正确的绝对日期、星期、年份或期间。",
        "six_level_anchors": {
            0: "核心相对日期、星期或年份解析完全失败",
            20: "答案主要依赖错误日期或年份",
            40: "关键日期/年份处理错误或含混",
            60: "大体正确但缺少时区、星期或绝对日期说明",
            80: "核心解析正确，存在轻微表达缺口",
            100: "基于请求时间和时区正确解析，并在答案中呈现必要日期",
        },
    },
    {
        "key": "market_calendar_status",
        "label_zh": "市场交易日历状态",
        "description": "评估最终回答是否判断对应市场、品种或证券在目标日期是否交易。",
        "six_level_anchors": {
            0: "休市日仍输出与真实交易状态冲突的结论",
            20: "严重混用市场日历或按开盘模板作答",
            40: "识别到交易日历线索，但目标日期/市场处理错误或含混",
            60: "知道可能涉及交易日历，但仅泛泛提示，未落实到目标日期/市场",
            80: "核心交易状态正确，存在次要边界未展开",
            100: "正确判断目标市场交易状态，区分休市、半日市、盘中/盘后和跨市场差异",
        },
    },
    {
        "key": "data_asof_freshness",
        "label_zh": "数据时点与新鲜度",
        "description": "评估最终回答是否说明数据日期，防止旧数据冒充当前事实。",
        "six_level_anchors": {
            0: "把旧数据包装成今天/最新事实，导致主结论冲突",
            20: "答案主要依赖旧数据且没有提示",
            40: "部分识别数据时点，但关键 as-of 处理错误或含混",
            60: "使用的数据大致可接受，但 as-of 说明不足",
            80: "核心 as-of 正确，存在轻微说明缺口",
            100: "明确数据 as-of，若当天无交易或无最新数据，说明使用上一交易日/最新可得数据的原因",
        },
    },
    {
        "key": "period_disclosure_mapping",
        "label_zh": "报告期与披露期映射",
        "description": "评估最终回答是否正确处理财报、分红、年度/季度/年中等报告期和披露期。",
        "six_level_anchors": {
            0: "报告期、年份或披露期映射完全错误",
            20: "因可得数据私自改写用户年份或期间",
            40: "关键报告期/披露期/实施日处理错误或含混",
            60: "报告期方向正确，但披露期或替代口径说明不完整",
            80: "核心映射正确，存在次要字段或限制说明缺口",
            100: "区分自然语言年份、财政/报告期、披露日期和最新可得数据；缺数据时先说明缺口再给替代",
        },
    },
    {
        "key": "premise_correction_clarification",
        "label_zh": "时间前提纠错与澄清",
        "description": "评估最终回答是否在用户时间前提错误或模糊时主动纠错。",
        "six_level_anchors": {
            0: "完全不纠错，顺着错误前提生成看似完整的错误答案",
            20: "只有极弱提示，用户仍会采信错误前提",
            40: "有纠错意图但未阻止核心误解",
            60: "有部分提示，但放在后文或没有充分阻止误解",
            80: "基本完成纠错，替代口径略不完整",
            100: "开头直接澄清错误前提，并给可用替代问法或可回答口径",
        },
    },
    {
        "key": "answer_composition_credibility",
        "label_zh": "答案组织与可信边界",
        "description": "评估最终回答是否让用户清楚理解时间口径和可信边界。",
        "six_level_anchors": {
            0: "模板化套话或堆行情指标，掩盖关键时间错误",
            20: "表达严重误导，让用户采信错误时间前提",
            40: "主结论中时间边界混乱，容易误解",
            60: "主结论可读，但时间边界散乱或容易误解",
            80: "表达清楚，存在轻微限制说明缺口",
            100: "日期、市场、数据时点、限制和替代口径表达清楚，不模板化",
        },
    },
]

# 默认权重（总和 100），LLM 动态权重回退时使用。
# 原过程侧权重已并入可从最终回答判断的交易状态、数据时点、纠错和表达维度。

DEFAULT_WEIGHTS = {
    "temporal_intent_recognition": 15,
    "anchor_date_resolution": 15,
    "market_calendar_status": 18,
    "data_asof_freshness": 18,
    "period_disclosure_mapping": 10,
    "premise_correction_clarification": 12,
    "answer_composition_credibility": 12,
}

WEIGHT_RULES: list[dict] = []

# 封顶标签（保留原类别标签语义，不直接修改分数）

CAP_RULES = [
    {
        "name": "hard_wrong_anchor_date",
        "label_zh": "核心日期锚点错误",
        "label_tag": "核心日期锚点错误",
        "severity": "critical",
        "ceiling": 40,
        "score_effect": "tag_only",
        "description": "核心相对日期、星期或年份解析错误，且该错误影响主结论。",
    },
    {
        "name": "market_closed_answered_as_open",
        "label_zh": "休市日按开盘回答",
        "label_tag": "休市日按开盘回答",
        "severity": "critical",
        "ceiling": 35,
        "score_effect": "tag_only",
        "description": "目标市场/品种在目标日期无交易，最终回答仍给出当日涨跌、开盘走势或交易结论，且未说明休市。",
    },
    {
        "name": "stale_data_masquerading_as_today",
        "label_zh": "旧数据冒充今天/最新",
        "label_tag": "旧数据冒充今天/最新",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "用旧行情、旧价格、旧公告或旧财报回答今天/最新问题，且最终回答未显式说明 as-of。",
    },
    {
        "name": "missing_required_premise_correction",
        "label_zh": "缺失必要前提纠错",
        "label_tag": "缺失必要前提纠错",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "用户问题的时间前提明显错误或不可成立，最终回答未先纠错，导致用户可能采信错误前提。",
    },
    {
        "name": "fiscal_period_disclosure_error",
        "label_zh": "财报/分红/报告期映射错误",
        "label_tag": "财报/分红/报告期映射错误",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "财报/分红/报告期映射错误，尤其把自然语言年份、报告期、披露日、分红实施日混淆。",
    },
    {
        "name": "fabricated_time_fact",
        "label_zh": "编造时间事实",
        "label_tag": "编造时间事实",
        "severity": "critical",
        "ceiling": 30,
        "score_effect": "tag_only",
        "description": "最终回答编造市场是否开盘、节假日、星期、数据日期、公告日期或报告期事实。",
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
