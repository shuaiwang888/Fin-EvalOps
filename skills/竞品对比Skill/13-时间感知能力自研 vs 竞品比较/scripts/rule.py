"""
13-time-awareness-ability-self-vs-competitor 评测规则定义。

该比较 skill 沿用第 13 类时间感知能力的绝对评分维度、权重、cap label 和根因体系；
pairwise 比较字段由输出 schema 约束。

权重分配、封顶规则、根因分类体系的结构化定义。
scoring.py 可使用这些规则将 LLM 的 raw_score 输出转换为完整 evaluation dict。
"""

# ── 维度定义 ────────────────────────────────────────────────────────────────

DIMENSIONS = [
    {
        "key": "temporal_intent_recognition",
        "label_zh": "时间意图识别",
        "description": "识别用户问题中的显式/隐式时间意图。",
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
        "description": "把相对时间解析到正确的绝对日期、星期、年份或期间。",
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
        "description": "判断对应市场、品种或证券在目标日期是否交易。",
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
        "description": "核验数据日期，防止旧数据冒充当前事实。",
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
        "description": "正确处理财报、分红、年度/季度/年中等报告期和披露期。",
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
        "description": "发现用户时间前提错误或模糊时主动纠错。",
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
        "description": "最终答案是否让用户清楚理解时间口径和可信边界。",
        "six_level_anchors": {
            0: "模板化套话或堆行情指标，掩盖关键时间错误",
            20: "表达严重误导，让用户采信错误时间前提",
            40: "主结论中时间边界混乱，容易误解",
            60: "主结论可读，但时间边界散乱或容易误解",
            80: "表达清楚，存在轻微限制说明缺口",
            100: "日期、市场、数据时点、限制和替代口径表达清楚，不模板化",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "链路是否正确使用工具核验时间、交易日历和数据时点。",
        "six_level_anchors": {
            0: "工具证据与答案相反，仍输出错误结论；或编造工具不可支持的时间事实",
            20: "应查却不查，或查错市场/日期/报告期",
            40: "工具调用不足或输入有明显瑕疵，导致答案时间边界含混",
            60: "工具方向正确但输入或读取不完整",
            80: "工具选择和主要输入正确，存在次要字段遗漏但不影响结论",
            100: "调用合适工具，输入包含正确市场/代码/日期/报告期，并正确读取返回日期",
        },
    },
]

# ── 权重规则 ────────────────────────────────────────────────────────────────

# 默认权重（总和 100），LLM 动态权重回退时使用；实际评测应按题目风险动态调整。
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

# 按 skill_name 匹配的权重规则，按顺序匹配第一个命中。
WEIGHT_RULES: list[dict] = []

# ── 封顶规则（v5: 改为标签标记，不修改分数） ────────────────────────────────

CAP_RULES = [
    {
        "name": "hard_wrong_anchor_date",
        "label_zh": "核心日期锚点错误",
        "label_tag": "核心日期锚点错误",
        "severity": "critical",
        "ceiling": 40,
        "description": "核心相对日期、星期或年份解析错误，且该错误影响主结论。",
    },
    {
        "name": "market_closed_answered_as_open",
        "label_zh": "休市日按开盘回答",
        "label_tag": "休市日按开盘回答",
        "severity": "critical",
        "ceiling": 35,
        "description": "目标市场/品种在目标日期无交易，答案仍给出当日涨跌、开盘走势或交易结论，且未说明休市。",
    },
    {
        "name": "stale_data_masquerading_as_today",
        "label_zh": "旧数据冒充今天/最新",
        "label_tag": "旧数据冒充今天/最新",
        "severity": "critical",
        "ceiling": 45,
        "description": "用旧行情、旧价格、旧公告或旧财报回答今天/最新问题，且最终答案未显式说明 as-of。",
    },
    {
        "name": "missing_required_premise_correction",
        "label_zh": "缺失必要前提纠错",
        "label_tag": "缺失必要前提纠错",
        "severity": "critical",
        "ceiling": 50,
        "description": "用户问题的时间前提明显错误或不可成立，答案未先纠错，导致用户可能采信错误前提。",
    },
    {
        "name": "fiscal_period_disclosure_error",
        "label_zh": "财报/分红/报告期映射错误",
        "label_tag": "财报/分红/报告期映射错误",
        "severity": "critical",
        "ceiling": 50,
        "description": "财报/分红/报告期映射错误，尤其把自然语言年份、报告期、披露日、分红实施日混淆。",
    },
    {
        "name": "fabricated_time_fact",
        "label_zh": "编造时间事实",
        "label_tag": "编造时间事实",
        "severity": "critical",
        "ceiling": 30,
        "description": "编造市场是否开盘、节假日、星期、数据日期、公告日期或报告期事实。",
    },
]

# ── 根因分类 ────────────────────────────────────────────────────────────────

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "时间意图理解",
        "description": "系统是否正确理解了用户问题中的时间意图、相对日期和市场/品种？",
        "l2": [
            "missed-temporal-intent",
            "wrong-relative-time-anchor",
            "ambiguous-time-not-clarified",
            "wrong-market-entity",
        ],
    },
    {
        "l1": "evidence",
        "l1_zh": "时间证据检索",
        "description": "系统是否找到正确、充分、可追溯的时间证据？",
        "l2": [
            "no-calendar-evidence",
            "stale-data-not-detected",
            "report-period-evidence-mismatch",
            "insufficient-asof-evidence",
        ],
    },
    {
        "l1": "tool",
        "l1_zh": "时间核验工具",
        "description": "系统是否选对工具、填对日期/市场/代码/报告期，并正确读取返回时间字段？",
        "l2": [
            "calendar-tool-missing",
            "wrong-tool-date-input",
            "tool-output-date-misread",
            "fallback-without-disclosure",
        ],
    },
    {
        "l1": "reasoning",
        "l1_zh": "时间推理",
        "description": "系统是否把自然日、交易日、报告期、披露期和市场状态推导成正确结论？",
        "l2": [
            "natural-day-trading-day-confusion",
            "fiscal-year-calendar-year-confusion",
            "premise-not-rejected",
            "date-weekday-inconsistency",
            "template-overrides-time-check",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "答案组织",
        "description": "关键日期、市场状态、as-of 和替代口径是否清楚呈现给用户？",
        "l2": [
            "asof-not-visible",
            "correction-buried",
            "misleading-current-tense",
        ],
    },
    {
        "l1": "capability_gap",
        "l1_zh": "能力或数据覆盖缺口",
        "description": "工具或数据源覆盖不足时，系统是否说明限制并采用谨慎替代？",
        "l2": [
            "market-calendar-coverage-gap",
            "disclosure-data-coverage-gap",
        ],
    },
]

# 低分维度 → 最可能的 L1 根因映射
ROOT_CAUSE_DIM_MAP = {
    "temporal_intent_recognition": "intent",
    "anchor_date_resolution": "intent",
    "market_calendar_status": "reasoning",
    "data_asof_freshness": "evidence",
    "period_disclosure_mapping": "reasoning",
    "premise_correction_clarification": "reasoning",
    "answer_composition_credibility": "composition",
    "tool_usage": "tool",
}
