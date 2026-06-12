"""
07-interactive-clarification 评测规则定义。

权重分配、封顶规则、根因分类体系的结构化定义。
scoring.py 可使用这些规则将 LLM 的 raw_score 输出转换为完整 evaluation dict。
"""

DIMENSIONS = [
    {
        "key": "intent_fulfillment",
        "label_zh": "意图满足度",
        "description": "评估答案是否识别并回应用户真实咨询目标，而不是只按字面问题或模板回答。",
        "six_level_anchors": {
            0: "完全答非所问，忽略用户真实咨询目标",
            20: "只触及表层意图，核心需求被替换或误解",
            40: "部分满足意图，但关键目标、隐含约束或投资问题缺失",
            60: "基本满足意图，但仍有明显遗漏或泛化",
            80: "很好满足意图，显性与主要隐含需求均覆盖",
            100: "完美满足意图，并把用户真实目标转化为清晰咨询闭环",
        },
    },
    {
        "key": "ambiguity_clarification",
        "label_zh": "模糊意图澄清",
        "description": "评估答案是否识别信息缺口、错误前提、模糊词和多义对象，并采用追问、假设分层或口径定义。",
        "six_level_anchors": {
            0: "该澄清时完全不澄清，直接在关键缺口上输出结论",
            20: "泛泛提示信息不足，但没有问到关键变量",
            40: "识别部分模糊点，但遗漏最影响结论的变量或前提",
            60: "能澄清主要缺口，但问题或假设不够精确",
            80: "澄清变量准确，能给出可继续推进的分层方案",
            100: "澄清、假设、直接可用的临时方案三者平衡，用户无需猜下一步",
        },
    },
    {
        "key": "context_continuity",
        "label_zh": "多轮承接闭环",
        "description": "评估答案是否承接历史上下文、用户补充信息和前轮模型承诺。",
        "six_level_anchors": {
            0: "完全忽略上下文，像新问题一样回答",
            20: "引用了上下文表面信息，但核心补充未进入方案",
            40: "承接部分信息，但前轮澄清框架与后续回答断裂",
            60: "基本承接上下文，有个别变量或承诺遗漏",
            80: "清晰继承前轮变量、假设和用户补充，方案连贯",
            100: "多轮上下文闭环完美，能解释新信息如何改变判断和行动",
        },
    },
    {
        "key": "entity_resolution",
        "label_zh": "标的与语义纠错",
        "description": "评估错别字、同音字、异常代码、简称和金融黑话的实体识别是否贴近股民真实输入习惯。",
        "six_level_anchors": {
            0: "实体识别完全错误，导致整答对象错位",
            20: "机械匹配到低概率实体，未发现明显错别字或代码异常",
            40: "发现异常但候选排序或澄清策略不合理",
            60: "基本识别正确实体，但提示、证据或备选说明不足",
            80: "正确识别最可能实体，并在必要时说明纠错依据或备选项",
            100: "实体纠错稳健，能综合市场概率、拼音/同音、用户语境和工具结果",
        },
    },
    {
        "key": "financial_rule_and_premise",
        "label_zh": "金融规则与前提纠错",
        "description": "评估答案是否识别交易规则、权限门槛、清算计息、税费和市场制度中的错误前提。",
        "six_level_anchors": {
            0: "关键金融规则错误，或在错误前提上继续给方案",
            20: "提到风险但没有纠正会使方案失效的核心前提",
            40: "纠正了部分规则，但遗漏关键限制、时间窗口或适用市场",
            60: "规则判断基本正确，但解释不够精确或缺少操作替代方案",
            80: "准确纠错并给出可行替代路径、时间窗口或操作约束",
            100: "规则、权限、税费、清算和用户目标全部打通，避免误导性操作",
        },
    },
    {
        "key": "assumption_definition",
        "label_zh": "假设口径与条件定义",
        "description": "评估答案是否把模糊金融条件转化为可核验指标、窗口、阈值和筛选逻辑。",
        "six_level_anchors": {
            0: "完全没有定义模糊条件，结论不可复核",
            20: "用了模糊口径或自造标准，未解释依据",
            40: "定义了部分条件，但时间窗、指标或阈值仍不清楚",
            60: "主要口径清楚，但个别阈值可商榷或前后一致性不足",
            80: "口径透明，能说明定义、局限和替代口径",
            100: "口径定义专业且可复现，能根据用户目标动态选择指标体系",
        },
    },
    {
        "key": "actionability_and_risk_plan",
        "label_zh": "澄清后落地与风险边界",
        "description": "评估答案是否在完成澄清或纠错后，把用户目标转化为可执行、可验证、有风险边界的下一步。",
        "six_level_anchors": {
            0: "没有可执行方案，或给出明显不可执行/误导性建议",
            20: "只有泛泛建议，没有触发条件、仓位、价格或观察指标",
            40: "有行动建议但缺少关键约束、风险边界或备选路径",
            60: "方案基本可执行，但细节、条件或风险提示不充分",
            80: "方案包含触发条件、节奏、风险控制和复盘指标",
            100: "行动闭环完整，能适配用户约束并提供可跟踪的后续动作",
        },
    },
    {
        "key": "evidence_grounding",
        "label_zh": "事实证据与数据支撑",
        "description": "评估答案使用的行情、财务、公告、交易规则、工具输出或资料来源是否准确充分。",
        "six_level_anchors": {
            0: "核心事实或数据错误，或编造不可验证信息",
            20: "证据严重不足，结论主要靠主观判断",
            40: "有证据但来源、时间或口径与问题不匹配",
            60: "主要证据可用，但关键数据、规则来源或交叉验证不足",
            80: "证据充分、口径清楚，能支持主要结论",
            100: "证据链完整且可复核，能把数据、规则和结论精确连接",
        },
    },
    {
        "key": "guidance_and_retention",
        "label_zh": "后续引导闭环",
        "description": "评估答案是否提供贴合当前咨询的后续追问、提醒、监控、复查或任务化建议。",
        "six_level_anchors": {
            0: "无后续引导，或引导与当前问题无关",
            20: "只有泛泛客套式引导",
            40: "有后续问题，但不能形成持续价值",
            60: "能提出相关下一步，但不够任务化或可执行",
            80: "后续引导贴合用户目标，包含监控、提醒或复查动作",
            100: "形成明确持续服务闭环，能自然推动下一轮高价值交互",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "评估规划链路中工具选择、参数、实体确认、规则查询和交叉验证是否合理高效。",
        "six_level_anchors": {
            0: "本应使用工具却完全未用，或工具结果全部错误",
            20: "工具选择明显错误，导致实体、规则或数据错误",
            40: "工具选择基本相关但参数、时间窗或候选实体有明显问题",
            60: "工具使用基本合理，但缺少必要交叉验证或有冗余",
            80: "工具选择精准，能确认实体、规则和关键数据",
            100: "工具链最小且充分，参数精确，能把工具结果正确融入回答",
        },
    },
    {
        "key": "latency_efficiency",
        "label_zh": "响应耗时与执行效率",
        "description": "评估交互澄清链路在质量达标前提下的响应速度和调用效率。",
        "six_level_anchors": {
            0: "严重超时或未完成",
            20: "耗时远超合理范围且质量仍差",
            40: "耗时偏长，有明显冗余调用或重复分析",
            60: "耗时基本可接受，但仍有优化空间",
            80: "耗时合理，链路较高效",
            100: "以最少必要步骤快速完成澄清、核验和回答",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_fulfillment": 12,
    "ambiguity_clarification": 16,
    "context_continuity": 14,
    "entity_resolution": 12,
    "financial_rule_and_premise": 14,
    "assumption_definition": 8,
    "actionability_and_risk_plan": 8,
    "evidence_grounding": 6,
    "guidance_and_retention": 5,
    "tool_usage": 3,
    "latency_efficiency": 2,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "wrong_financial_rule_or_unhandled_invalid_premise",
        "label_zh": "金融规则错误或错误前提未纠正",
        "label_tag": "规则/前提硬错",
        "severity": "critical",
        "ceiling": 40,
        "description": "交易规则、权限、税费、计息或市场制度错误，或在错误前提上继续给操作方案。",
    },
    {
        "name": "wrong_entity_resolution",
        "label_zh": "标的识别错误",
        "label_tag": "标的识别错误",
        "severity": "critical",
        "ceiling": 45,
        "description": "错别字、异常代码或简称识别为错误股票/产品，导致整答对象错位。",
    },
    {
        "name": "fabricated_or_unsupported_specific_advice",
        "label_zh": "缺证据的具体交易建议",
        "label_tag": "无证据交易建议",
        "severity": "critical",
        "ceiling": 50,
        "description": "给出具体买卖、满仓、止盈止损、股票推荐或价格判断，但缺少必要事实、规则和风险边界。",
    },
    {
        "name": "context_break_after_clarification",
        "label_zh": "澄清后二轮承接断裂",
        "label_tag": "多轮承接断裂",
        "severity": "warning",
        "ceiling": 55,
        "description": "首轮澄清建立了变量或框架，但用户补充后答案没有沿该框架推进。",
    },
    {
        "name": "missing_required_clarification",
        "label_zh": "遗漏必要澄清",
        "label_tag": "缺必要澄清",
        "severity": "warning",
        "ceiling": 60,
        "description": "用户关键信息缺失或多义，答案却直接给确定结论。",
    },
    {
        "name": "inconsistent_time_or_definition_scope",
        "label_zh": "时间或定义口径不一致",
        "label_tag": "口径不一致",
        "severity": "warning",
        "ceiling": 65,
        "description": "同一答案中对近期、短线、市值适中、回调较多等口径前后不一致。",
    },
    {
        "name": "generic_template_without_clarification_value",
        "label_zh": "模板化答复无咨询价值",
        "label_tag": "模板化无闭环",
        "severity": "warning",
        "ceiling": 70,
        "description": "答案套用基本面/技术面/资金面模板，未处理用户本次咨询的真实问题。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "理解问题",
        "description": "系统是否识别了用户真实咨询目标和隐含需求？",
        "l2": ["surface_intent_only", "hidden_need_missed", "sub_question_omitted", "risk_intent_missed"],
    },
    {
        "l1": "context",
        "l1_zh": "承接上下文",
        "description": "系统是否正确使用了历史轮次、用户补充和前轮承诺？",
        "l2": ["prior_turn_ignored", "clarification_not_followed", "user_variables_dropped", "context_state_conflict"],
    },
    {
        "l1": "evidence",
        "l1_zh": "检索证据",
        "description": "系统获取的事实、规则、实体和行情数据是否正确充分？",
        "l2": ["insufficient_evidence", "wrong_rule_source", "wrong_entity_evidence", "outdated_or_mismatched_data"],
    },
    {
        "l1": "tool",
        "l1_zh": "选择与执行工具",
        "description": "系统是否选对工具、参数、时间窗和实体候选？",
        "l2": ["wrong_tool_selection", "wrong_tool_params", "missing_tool_call", "inefficient_tool_chain", "overreliance_on_nlu"],
    },
    {
        "l1": "reasoning",
        "l1_zh": "金融推理",
        "description": "系统是否完成错误前提检查、规则推理、口径定义和行动方案推导？",
        "l2": ["premise_not_checked", "ambiguity_not_decomposed", "trading_rule_reasoning_error", "threshold_definition_weak", "causal_order_reversed"],
    },
    {
        "l1": "composition",
        "l1_zh": "组织答案",
        "description": "逻辑可能存在但是否在答案中清晰呈现并形成咨询闭环？",
        "l2": ["generic_template", "missing_direct_answer", "unclear_structure", "next_step_guidance_missing", "risk_boundary_missing"],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "intent_fulfillment": "intent",
    "ambiguity_clarification": "reasoning",
    "context_continuity": "context",
    "entity_resolution": "evidence",
    "financial_rule_and_premise": "reasoning",
    "assumption_definition": "reasoning",
    "actionability_and_risk_plan": "composition",
    "evidence_grounding": "evidence",
    "guidance_and_retention": "composition",
    "tool_usage": "tool",
    "latency_efficiency": "tool",
}
