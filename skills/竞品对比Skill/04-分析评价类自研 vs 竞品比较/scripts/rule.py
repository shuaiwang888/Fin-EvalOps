"""
04-analysis-evaluation-and-self-judgment 评测规则定义 (v5)。

分析评价类问题：识别投资决策需求，选择合适的评价维度。
"""

DIMENSIONS = [
    {
        "key": "intent_scenario_recognition", "label_zh": "意图和场景识别",
        "description": "评估答案是否准确识别了用户的投资场景和真实决策需求。始终考察。",
        "six_level_anchors": {
            0: "完全没有识别投资场景或决策需求",
            20: "将投资分析问题误判为简单问答，场景识别严重偏离",
            40: "识别了大致方向但遗漏了关键的场景约束或决策类型",
            60: "场景识别基本正确，但隐含的决策需求未充分挖掘",
            80: "准确识别了投资场景和决策需求，分析框架与之匹配",
            100: "完美识别所有显性和隐性场景要素，决策需求定位精准",
        },
    },
    {
        "key": "evidence_source_quality", "label_zh": "证据来源质量",
        "description": "评估引用的证据来源是否关键、充分、专业。",
        "six_level_anchors": {
            0: "完全没有引用证据或引用的证据来源完全不相关",
            20: "引用的证据来源浅层、不专业，缺少关键信源",
            40: "有部分专业信源但遗漏了该分析场景下最核心的证据类型",
            60: "证据来源基本恰当，但覆盖不足或个别来源权威性不够",
            80: "证据来源专业、关键、充分，覆盖了分析所需的主要信源",
            100: "证据来源完美，多层级信源交叉验证，权威性无可挑剔",
        },
    },
    {
        "key": "recency_time_boundary", "label_zh": "时效性和时间边界",
        "description": "评估答案是否严格遵守时效要求和时间边界。",
        "six_level_anchors": {
            0: "完全无视时效要求，引用明显过时信息",
            20: "有时效意识但关键数据的时间窗口严重不匹配",
            40: "时效基本合规但个别证据过时或时间边界有偏差",
            60: "时效把握良好但最新的关键信息可能未被纳入",
            80: "时效控制好，时间边界明确，所有证据均在有效时间窗口内",
            100: "时效完美，精确匹配用户时间要求，最新信息全面覆盖",
        },
    },
    {
        "key": "investment_logic_depth", "label_zh": "投资逻辑深度",
        "description": "评估分析是否从信息深入到投资判断和因果链。始终考察。",
        "six_level_anchors": {
            0: "完全停留在信息罗列层面，没有任何投资逻辑推导",
            20: "有少量逻辑线索但没有形成完整的投资判断链",
            40: "有投资逻辑但停留在浅层，缺少因果深挖或多情景推演",
            60: "投资逻辑基本成型但缺少关键维度的深度分析",
            80: "投资逻辑深入，因果链完整，多维度分析充分",
            100: "投资逻辑深邃，层层递进，多情景推演完整，结论有穿透力",
        },
    },
    {
        "key": "method_fit", "label_zh": "分析方法匹配",
        "description": "评估分析方法与用户问题类型的匹配度。始终考察。",
        "six_level_anchors": {
            0: "分析方法完全不匹配问题类型",
            20: "使用了错误的分析框架或方法，方向根本不对",
            40: "方法大致可接受但与问题的最优分析方法存在明显偏差",
            60: "方法基本匹配，但可以选用更合适的分析工具或框架",
            80: "分析方法得当，与问题类型高度匹配",
            100: "分析方法完美匹配，且创造性地组合了多种框架以达到最优分析效果",
        },
    },
    {
        "key": "comparison_quantification", "label_zh": "对比和量化",
        "description": "评估是否提供了量化比较、排序和取舍依据。",
        "six_level_anchors": {
            0: "完全没有量化比较，纯文字描述",
            20: "有比较意图但无具体数据支撑或比较维度杂乱",
            40: "有量化数据但没有形成系统的对比分析或排序",
            60: "有基本的量化比较但深度不够，或缺少关键对比维度",
            80: "量化比较系统全面，排序有据，对比维度丰富",
            100: "量化比较完美，多维度交叉对比，置信区间/敏感性分析完整",
        },
    },
    {
        "key": "actionability_risk", "label_zh": "可执行性和风险",
        "description": "评估答案是否给出了可执行的投资判断和风险边界。",
        "six_level_anchors": {
            0: "完全没有可执行建议或风险提示",
            20: "给出了模糊建议但没有任何可执行细节或风险考量",
            40: "有可执行方向但缺少具体的触发条件、仓位或风控边界",
            60: "可执行性基本具备但风险考量不够全面",
            80: "可执行建议明确，风险边界清晰，触发条件和止损有据",
            100: "可执行性完美，建议具体到仓位/时点/条件，风险模型完整",
        },
    },
    {
        "key": "composition_credibility", "label_zh": "表达可信度",
        "description": "评估答案表达是否可信、客观。始终为辅助维度。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导信息",
            20: "表达模糊空洞，大量无根据的断言",
            40: "有可信内容但掺杂主观臆断或缺少证据支撑",
            60: "表达基本可信客观，但个别结论语气过于绝对",
            80: "表达可信、客观、审慎，证据与结论匹配良好",
            100: "表达完美，每项结论有证据，语气专业审慎，无任何夸大",
        },
    },
    {
        "key": "tool_usage", "label_zh": "工具使用合理性",
        "description": "评估工具选择和使用是否合理。始终考察，在链路诊断阶段评分。",
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
    "intent_scenario_recognition": 15,
    "evidence_source_quality": 15,
    "recency_time_boundary": 10,
    "investment_logic_depth": 20,
    "method_fit": 12,
    "comparison_quantification": 10,
    "actionability_risk": 8,
    "composition_credibility": 5,
    "tool_usage": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missed_core_investment_logic", "label_zh": "遗漏核心投资逻辑",
        "label_tag": "遗漏核心投资逻辑", "severity": "critical", "ceiling": 60,
        "description": "答案未触及用户问题的核心投资逻辑。",
    },
    {
        "name": "stale_or_wrong_time_evidence", "label_zh": "时效错误或过时证据",
        "label_tag": "时效错误/过时证据", "severity": "critical", "ceiling": 50,
        "description": "引用的证据存在时效性错误或明显过时。",
    },
    {
        "name": "method_mismatch", "label_zh": "分析方法不匹配",
        "label_tag": "分析方法不匹配", "severity": "warning", "ceiling": 55,
        "description": "使用的分析方法与用户问题的类型不匹配。",
    },
    {
        "name": "template_data_dump", "label_zh": "模板化数据堆砌",
        "label_tag": "模板化数据堆砌", "severity": "warning", "ceiling": 60,
        "description": "答案变成数据罗列而没有实质性分析。",
    },
    {
        "name": "missing_required_analysis_elements", "label_zh": "遗漏必要分析要素",
        "label_tag": "遗漏必要分析要素", "severity": "warning", "ceiling": 65,
        "description": "用户问题明确需要的分析要素未覆盖。",
    },
    {
        "name": "wrong_or_shallow_source", "label_zh": "证据来源错误或浅层",
        "label_tag": "证据来源错误/浅层", "severity": "critical", "ceiling": 55,
        "description": "引用的证据来源不当或停留在浅层信息。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "理解问题", "description": "是否识别真实投资场景和必备要素", "l2": ["scenario_misjudged", "missing_required_element"]},
    {"l1": "evidence", "l1_zh": "检索信息", "description": "找到的信息是否关键、充分、专业、时效正确", "l2": ["shallow_source", "outdated_evidence", "missing_key_evidence"]},
    {"l1": "tool", "l1_zh": "选择与执行工具", "description": "是否选对工具、写对输入、用足链路", "l2": ["wrong_tool", "insufficient_tool_chain", "tool_param_error"]},
    {"l1": "reasoning", "l1_zh": "推导投资逻辑", "description": "是否把信息转成投资判断和因果链", "l2": ["weak_causal_chain", "missing_synthesis", "shallow_logic"]},
    {"l1": "composition", "l1_zh": "组织答案", "description": "最终答案是否把关键逻辑讲清楚", "l2": ["template_output", "unclear_narrative", "data_dump"]},
    {"l1": "capability_gap", "l1_zh": "数据源/能力缺口", "description": "当前工具或数据源缺少必要深层资料", "l2": ["missing_deep_data", "tool_capability_limit"]},
]

ROOT_CAUSE_DIM_MAP = {
    "intent_scenario_recognition": "intent",
    "evidence_source_quality": "evidence",
    "recency_time_boundary": "evidence",
    "investment_logic_depth": "reasoning",
    "method_fit": "reasoning",
    "comparison_quantification": "reasoning",
    "actionability_risk": "reasoning",
    "composition_credibility": "composition",
    "tool_usage": "tool",
}

