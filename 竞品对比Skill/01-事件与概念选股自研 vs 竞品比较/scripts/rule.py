"""
01-event-and-concept-stock-selection-self-vs-competitor 评测规则定义。

该比较 skill 定义了事件/概念选股领域的绝对评分维度、权重、封顶标签和根因体系；
pairwise 比较字段由输出 schema 约束。

权重分配、封顶规则、根因分类体系的结构化定义。
scoring.py 使用这些规则将 LLM 的 raw_score 输出转换为完整 evaluation dict。
"""

# ── 维度定义 ────────────────────────────────────────────────────────────────

DIMENSIONS = [
    {
        "key": "intent_fulfillment",
        "label_zh": "意图满足度",
        "description": "评估答案是否完整、准确地满足了用户的提问意图。所有题目均考察。",
        "six_level_anchors": {
            0: "完全未响应用户意图，答案与问题无关或直接拒答",
            20: "仅触及意图的某个边角，遗漏了用户的核心需求",
            40: "部分满足意图但关键需求缺失或偏差较大",
            60: "基本满足意图，有可改进的明显不足但方向正确",
            80: "很好地满足意图，逻辑完整、覆盖全面，仅有极轻微遗漏",
            100: "完美满足意图，所有显性和隐性需求均被覆盖，无任何可挑剔之处",
        },
    },
    {
        "key": "event_abstraction",
        "label_zh": "事件抽象度",
        "description": "评估答案是否正确识别并抽象了问题中隐含的事件/催化剂/政策/地缘因素。",
        "six_level_anchors": {
            0: "完全没有识别或抽象任何事件/催化剂因素",
            20: "提到了相关事件但抽象层次混乱，无法形成有效分析框架",
            40: "做了事件抽象但遗漏了核心驱动因素或混淆了主次",
            60: "正确抽象了主要事件，但次级因素或传导链条有缺失",
            80: "准确抽象了事件体系，主次分明，仅有极微小的遗漏",
            100: "事件抽象精准且完整，所有驱动因素和传导关系被清晰解构",
        },
    },
    {
        "key": "industry_mapping",
        "label_zh": "产业链映射",
        "description": "评估答案是否将事件正确映射到受益产业链环节和标的。",
        "six_level_anchors": {
            0: "完全没有做产业链映射，或映射完全错误",
            20: "仅给了泛泛的板块名称，没有产业链环节和逻辑",
            40: "指出了产业链但环节定位不准或遗漏了关键受益环节",
            60: "产业链映射基本正确，但缺少受益程度分层或个别环节有误",
            80: "产业链映射精准，环节清晰，受益逻辑完整",
            100: "产业链映射完美，上游/中游/下游/配套环节全解构，受益标的精准匹配",
        },
    },
    {
        "key": "ranking_judgment",
        "label_zh": "排序判断",
        "description": "评估答案是否按用户要求的排序/排名/优先级维度组织结果。",
        "six_level_anchors": {
            0: "用户要求排序但答案完全未提供，或排序逻辑完全错误",
            20: "有排序的意图但排序维度不明确或标准混乱",
            40: "有排序但排序标准与用户要求不匹配，或遗漏了关键排序维度",
            60: "排序基本符合要求，但排序理由不够充分或个别次序可商榷",
            80: "排序清晰有据，维度匹配用户意图，逻辑自洽",
            100: "排序完美，多维度交叉验证，排序标准透明且有充分证据支撑",
        },
    },
    {
        "key": "logic_closure",
        "label_zh": "逻辑闭环",
        "description": "评估答案从事件→传导路径→标的含义的逻辑链是否完整、无跳跃。",
        "six_level_anchors": {
            0: "逻辑链完全断裂，事件与结论之间无任何连接",
            20: "存在大量逻辑跳跃，关键环节缺失，结论悬浮",
            40: "有逻辑链但核心传导环节断裂或推导存在明显漏洞",
            60: "逻辑链基本完整，但个别环节的论证不够充分",
            80: "逻辑链完整且严密，从事件到结论层层递进，仅有极细微缺失",
            100: "逻辑闭环完美，每个推理步骤均有证据支撑，链条无懈可击",
        },
    },
    {
        "key": "timeliness_fact_boundary",
        "label_zh": "时效性与事实边界",
        "description": "评估答案是否严格遵守时间范围约束、事实边界准确。",
        "six_level_anchors": {
            0: "完全无视时间约束，或事实严重错误导致结论不可靠",
            20: "时效性考虑不足，引用了明显过时的信息或事实有多处偏差",
            40: "有时效意识但关键时间窗口判断有误，或部分事实边界模糊",
            60: "时效性和事实基本合规，但个别数据点或时间节点精度不足",
            80: "时效性把握好，事实边界清晰，引用准确",
            100: "时效性和事实边界完美，精确匹配用户时间约束，所有事实可查证",
        },
    },
    {
        "key": "credibility_expression",
        "label_zh": "可信度与表达",
        "description": "评估答案的表达是否可信、客观，是否避免了模糊断言。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导或虚假信息",
            20: "表达模糊空洞，大量无根据的断言，可信度很低",
            40: "有部分可信内容但掺杂了主观臆断或未经验证的陈述",
            60: "表达基本可信客观，但个别断言的证据支撑不足",
            80: "表达可信、客观、审慎，证据与结论匹配良好",
            100: "表达完美，每项结论均有明确证据，语气审慎专业，无可挑剔",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "评估答案涉及的规划链路中工具选择和使用是否合理、高效。",
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

# ── 权重规则 ────────────────────────────────────────────────────────────────

# 默认权重（总和 100），LLM 动态权重回退时使用
DEFAULT_WEIGHTS = {
    "intent_fulfillment": 20,
    "event_abstraction": 15,
    "industry_mapping": 10,
    "ranking_judgment": 15,
    "logic_closure": 15,
    "timeliness_fact_boundary": 10,
    "credibility_expression": 5,
    "tool_usage": 10,
}

# 按 skill_name 匹配的权重规则，按顺序匹配第一个命中
WEIGHT_RULES: list[dict] = [
    # 示例：如果 skill_name 为特定类型，可以覆盖默认权重
    # {"skill_name": "条件选股", "weights": {"ranking_judgment": 20, ...}},
]

# ── 封顶规则（v5: 改为标签标记，不修改分数） ────────────────────────────────

CAP_RULES = [
    {
        "name": "hard_time_or_fact_error",
        "label_zh": "硬性时间或事实错误",
        "label_tag": "硬性时间/事实错误",
        "severity": "critical",
        "ceiling": 40,  # v4 遗留，v5 仅作参考元数据
        "description": "关键年份、日期或时间范围有实质性错误，或事实/边界错误打破推荐可信度。",
    },
    {
        "name": "missing_required_ranking",
        "label_zh": "遗漏必要排序",
        "label_tag": "遗漏必要排序",
        "severity": "critical",
        "ceiling": 60,
        "description": "用户明确要求排序、排列或优先级，但答案未提供。",
    },
    {
        "name": "data_dump_without_core_rationale",
        "label_zh": "数据堆砌无核心论证",
        "label_tag": "数据堆砌无核心论证",
        "severity": "warning",
        "ceiling": 55,
        "description": "答案主要输出股票列表/表格/数据，没有解释核心受益逻辑。",
    },
    {
        "name": "wrong_evidence_type",
        "label_zh": "证据类型错误",
        "label_tag": "证据类型错误",
        "severity": "critical",
        "ceiling": 50,
        "description": "用户要求事件/新闻驱动的机会，但答案依赖了错误的证据类型。",
    },
    {
        "name": "unverifiable_subjective_expression",
        "label_zh": "不可验证的主观表达",
        "label_tag": "不可验证的主观表达",
        "severity": "warning",
        "ceiling": 65,
        "description": "答案依赖模糊、主观或缺乏支撑的断言，实质性降低可信度。",
    },
    {
        "name": "forced_mapping_or_entity_boundary_error",
        "label_zh": "强行映射或实体边界错误",
        "label_tag": "强行映射或实体边界错误",
        "severity": "critical",
        "ceiling": 50,
        "description": "强行将产业链/行业/概念映射到不匹配的标的，或没有区分主营/副业、直接/间接供应链、品牌/代工、核心/边缘等实体边界。",
    },
]

# ── 根因分类 ────────────────────────────────────────────────────────────────

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "意图理解",
        "description": "系统是否正确理解了用户要什么？",
        "l2": ["intent_misjudged", "sub_question_omitted"],
    },
    {
        "l1": "evidence",
        "l1_zh": "信息检索",
        "description": "系统找到的信息是否正确、充分、时效对？",
        "l2": ["insufficient_evidence", "outdated_evidence", "wrong_evidence_source"],
    },
    {
        "l1": "tool",
        "l1_zh": "工具选择与执行",
        "description": "系统是否选对了工具、用对了工具？",
        "l2": ["wrong_tool_selection", "wrong_tool_params", "missing_tool_call"],
    },
    {
        "l1": "reasoning",
        "l1_zh": "推理逻辑",
        "description": "事件→传导路径→标的含义的逻辑链是否完整？",
        "l2": [
            "no_ranking_criterion",
            "weak_causal_chain",
            "missing_beneficiary_logic",
            "shallow_event_abstraction",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "答案组织",
        "description": "逻辑可能存在但答案是否呈现出来了？",
        "l2": ["data_dump_no_narrative", "unclear_structure", "missing_key_context"],
    },
]

# 低分维度 → 最可能的 L1 根因映射
ROOT_CAUSE_DIM_MAP = {
    "intent_fulfillment": "intent",
    "event_abstraction": "reasoning",
    "industry_mapping": "reasoning",
    "ranking_judgment": "reasoning",
    "logic_closure": "reasoning",
    "timeliness_fact_boundary": "evidence",
    "credibility_expression": "composition",
    "tool_usage": "tool",
}


