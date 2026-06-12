"""
04-analysis-evaluation-and-self-judgment result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义分析评价类金融问答的最终回答质量维度、默认权重和质量标签。
pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_scenario_recognition",
        "label_zh": "意图和场景识别",
        "description": "评估最终回答是否准确识别用户的投资场景和真实决策需求。",
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
        "key": "evidence_source_quality",
        "label_zh": "证据来源质量",
        "description": "评估最终回答引用或呈现的证据来源是否关键、充分、专业。",
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
        "key": "recency_time_boundary",
        "label_zh": "时效性和时间边界",
        "description": "评估最终回答是否严格遵守时效要求和时间边界。",
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
        "key": "investment_logic_depth",
        "label_zh": "投资逻辑深度",
        "description": "评估最终回答是否从信息深入到投资判断和因果链。",
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
        "key": "method_fit",
        "label_zh": "分析方法匹配",
        "description": "评估最终回答的分析方法与用户问题类型、标的属性和投资周期是否匹配。",
        "six_level_anchors": {
            0: "分析方法完全不匹配问题类型",
            20: "使用了错误的分析框架或方法，方向根本不对",
            40: "方法大致可接受但与问题的最优分析方法存在明显偏差",
            60: "方法基本匹配，但可以选用更合适的分析方法或框架",
            80: "分析方法得当，与问题类型高度匹配",
            100: "分析方法完美匹配，且创造性地组合了多种框架以达到最优分析效果",
        },
    },
    {
        "key": "comparison_quantification",
        "label_zh": "对比和量化",
        "description": "评估最终回答是否提供了量化比较、排序和取舍依据。",
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
        "key": "actionability_risk",
        "label_zh": "可执行性和风险",
        "description": "评估最终回答是否给出了可执行的投资判断、触发条件和风险边界。",
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
        "key": "user_profile_suitability",
        "label_zh": "用户画像适配",
        "description": "评估最终回答是否把投资分析转化为适合用户风险、目标、期限、资金、持仓和成本约束的建议。",
        "six_level_anchors": {
            0: "完全无视用户明示的画像、资金、目标、期限或持仓约束",
            20: "只给通用建议，几乎没有体现用户适配",
            40: "有少量用户适配意识，但关键约束缺失或与建议不一致",
            60: "基本考虑了用户适配，但仓位、期限、组合角色或风险边界不够清楚",
            80: "用户适配充分，建议能体现风险目标、资金和组合角色约束",
            100: "用户适配完美，清楚解释为何适合该用户，并给出分层、仓位和风险边界",
        },
    },
    {
        "key": "scenario_emotion_recognition",
        "label_zh": "场景与情绪识别",
        "description": "评估最终回答是否识别用户浮亏、套牢、迷茫、急于回本等真实投资处境，并降低错误决策风险。",
        "six_level_anchors": {
            0: "完全误读亏损或情绪处境，并诱导继续高风险操作",
            20: "识别到少量情绪信号，但仍按普通荐股或短线机会处理",
            40: "能看出用户处境，但缺少降风险、复盘和纪律框架",
            60: "基本识别用户处境，并给出部分风险控制建议",
            80: "较好识别情绪和投资状态，能转化为稳健的行动框架",
            100: "完美识别用户处境，先稳定决策纪律，再给分层动作和风险边界",
        },
    },
    {
        "key": "composition_credibility",
        "label_zh": "表达可信度",
        "description": "评估最终回答表达是否可信、客观、审慎、非模板化。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导信息",
            20: "表达模糊空洞，大量无根据的断言",
            40: "有可信内容但掺杂主观臆断或缺少证据支撑",
            60: "表达基本可信客观，但个别结论语气过于绝对",
            80: "表达可信、客观、审慎，证据与结论匹配良好",
            100: "表达完美，每项结论有证据，语气专业审慎，无任何夸大",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_scenario_recognition": 14,
    "evidence_source_quality": 14,
    "recency_time_boundary": 9,
    "investment_logic_depth": 18,
    "method_fit": 11,
    "comparison_quantification": 8,
    "actionability_risk": 9,
    "user_profile_suitability": 8,
    "scenario_emotion_recognition": 4,
    "composition_credibility": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missed_core_investment_logic",
        "label_zh": "遗漏核心投资逻辑",
        "label_tag": "遗漏核心投资逻辑",
        "severity": "critical",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答未触及用户问题的核心投资逻辑。",
    },
    {
        "name": "stale_or_wrong_time_evidence",
        "label_zh": "时效错误或过时证据",
        "label_tag": "时效错误/过时证据",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答引用或依赖的证据存在时效性错误或明显过时。",
    },
    {
        "name": "method_mismatch",
        "label_zh": "分析方法不匹配",
        "label_tag": "分析方法不匹配",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答使用的分析方法与用户问题、标的属性或投资周期不匹配。",
    },
    {
        "name": "template_data_dump",
        "label_zh": "模板化数据堆砌",
        "label_tag": "模板化数据堆砌",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答变成模板化数据罗列或资讯拼接，没有实质性投资分析。",
    },
    {
        "name": "missing_required_analysis_elements",
        "label_zh": "遗漏必要分析要素",
        "label_tag": "遗漏必要分析要素",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "用户问题明确需要的分析要素未覆盖，例如基金回撤/同类比较、估值历史位置或切换对比。",
    },
    {
        "name": "wrong_or_shallow_source",
        "label_zh": "证据来源错误或浅层",
        "label_tag": "证据来源错误/浅层",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答引用的证据来源不当、浅层或无法支撑核心投资结论。",
    },
    {
        "name": "missing_user_profile_fit",
        "label_zh": "个人化建议缺少画像适配",
        "label_tag": "个人化建议缺少画像适配",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "用户明确要求个人化推荐或结合自身情况决策，但最终回答没有体现用户问题中明示的画像、目标、风险、资金、期限或持仓约束。",
    },
    {
        "name": "misread_loss_or_emotion_context",
        "label_zh": "误读亏损/情绪场景",
        "label_tag": "误读亏损/情绪场景",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答误读用户亏损、套牢、迷茫或急于回本处境，把风险控制问题当成普通荐股入口。",
    },
    {
        "name": "overconfident_or_unsuitable_action",
        "label_zh": "过度确定或不适当行动建议",
        "label_tag": "过度确定/不适当行动",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答给出过度确定或明显不适当的行动建议，可能诱导用户承担与问题场景不匹配的风险。",
    },
    {
        "name": "missing_decision_action_for_recommendation",
        "label_zh": "推荐/交易请求缺少行动输出",
        "label_tag": "推荐/交易请求缺少行动输出",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "用户要求推荐、买卖、持有、切换、仓位或解套，但最终回答没有给出可执行动作、触发条件或风险边界。",
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
