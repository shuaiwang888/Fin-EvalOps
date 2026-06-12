"""
05-kyc-recommendation-suggestions 评测规则定义 (v5)。

KYC 推荐建议类问题：判断用户投资决策需求，评估是否主动使用 KYC 数据。
"""

DIMENSIONS = [
    {
        "key": "intent_profile_understanding", "label_zh": "意图与画像理解",
        "description": "评估答案是否准确理解了用户意图并使用 KYC 画像数据。始终考察。",
        "six_level_anchors": {
            0: "完全未理解用户意图，答案与用户情况无关",
            20: "只是泛泛回答，与用户的具体画像和意图几乎无关",
            40: "部分触及意图但遗漏了关键画像维度或意图核心",
            60: "基本理解意图和画像，但个别画像要素未充分利用",
            80: "准确理解意图，画像数据使用充分，回答与用户高度匹配",
            100: "完美理解意图和画像，所有 KYC 维度均被充分利用，回答精准匹配",
        },
    },
    {
        "key": "scenario_emotion_recognition", "label_zh": "场景与情绪识别",
        "description": "评估是否识别了用户的情绪状态（亏损/套牢/迷茫/焦虑）。",
        "six_level_anchors": {
            0: "完全没有识别用户情绪状态",
            20: "察觉了情绪但处理不当（如对亏损用户给出过于乐观的建议）",
            40: "识别了情绪但给出的回应与情绪场景不完全匹配",
            60: "情绪识别基本到位，但回应中的情绪安抚或共情不够自然",
            80: "准确识别情绪场景，回应既安抚情绪又给出理性建议",
            100: "完美共情，准确捕捉情绪细微层次，回应兼顾心理需求和投资理性",
        },
    },
    {
        "key": "suitability_personalization", "label_zh": "适当性与个性化",
        "description": "评估推荐是否匹配用户风险偏好、投资期限和收益目标。始终考察。",
        "six_level_anchors": {
            0: "推荐完全不适合该用户，风险等级/投资期限明显不匹配",
            20: "推荐方向与用户画像存在重大偏差",
            40: "推荐大致方向可行但缺少对用户个别关键约束的考量",
            60: "推荐基本适合用户，但个性化程度不够或风险匹配不够精细",
            80: "推荐高度个性化，与用户风险偏好/期限/目标精准匹配",
            100: "推荐完美适配，每个建议都有明确的适配理由，考虑周全",
        },
    },
    {
        "key": "evidence_integration", "label_zh": "多维证据整合",
        "description": "评估是否整合了市场、宏观、行业、估值、技术等多维证据。",
        "six_level_anchors": {
            0: "完全没有证据支撑，纯主观建议",
            20: "仅有一两个泛泛的证据点，不足以支撑推荐结论",
            40: "有一定证据但维度单一，缺少多维度交叉验证",
            60: "多维证据基本具备但整合力度不足，各证据关联不够",
            80: "多维证据充分整合，相互印证，支撑推荐逻辑",
            100: "证据整合完美，多维度数据交叉验证，形成立体的推荐依据",
        },
    },
    {
        "key": "decision_actionability", "label_zh": "决策可执行性",
        "description": "评估推荐是否给出了可执行的操作建议（买卖/持有/仓位/配置）。",
        "six_level_anchors": {
            0: "完全没有可执行建议",
            20: "给出了方向性建议但没有任何操作细节",
            40: "有操作建议但缺少关键的仓位/时机/条件细节",
            60: "操作建议基本可执行但个别的触发条件或边界不够明确",
            80: "操作建议清晰可执行，仓位/时机/条件明确",
            100: "操作建议完美，每一步都有明确的执行条件和备选方案",
        },
    },
    {
        "key": "risk_boundary_control", "label_zh": "风险控制与边界",
        "description": "评估是否给出了风险边界和止损/风控建议。始终考察。",
        "six_level_anchors": {
            0: "完全没有风险提示或边界控制",
            20: "有风险提及但流于形式，没有实质性的风控措施",
            40: "有风控方向但缺少具体的止损位或风险阈值",
            60: "风险边界基本清晰但极端情景或尾部风险未充分警示",
            80: "风险边界明确，止损/风控措施具体可执行",
            100: "风控完美，多情景压力测试，止损/仓位管理/对冲方案一应俱全",
        },
    },
    {
        "key": "composition_credibility", "label_zh": "表达可信度",
        "description": "评估答案表达是否可信、审慎。始终为辅助维度。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导信息",
            20: "表达模糊空洞，大量无根据的断言",
            40: "有可信内容但掺杂主观臆断或过度确定的表述",
            60: "表达基本可信审慎，但个别结论的语气过于绝对",
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
    "intent_profile_understanding": 18,
    "scenario_emotion_recognition": 10,
    "suitability_personalization": 18,
    "evidence_integration": 14,
    "decision_actionability": 16,
    "risk_boundary_control": 12,
    "composition_credibility": 5,
    "tool_usage": 7,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missing_kyc_profile", "label_zh": "未使用KYC画像",
        "label_tag": "未使用KYC画像", "severity": "critical", "ceiling": 60,
        "description": "链路和答案都看不出主动使用用户 KYC 数据。",
    },
    {
        "name": "misread_emotional_loss_context", "label_zh": "误读亏损/情绪场景",
        "label_tag": "误读亏损/情绪场景", "severity": "critical", "ceiling": 50,
        "description": "忽略了用户的亏损、套牢或焦虑情绪状态。",
    },
    {
        "name": "fabricated_user_profile", "label_zh": "虚构用户画像",
        "label_tag": "虚构用户画像", "severity": "critical", "ceiling": 55,
        "description": "使用了不存在的或编造的用户画像信息。",
    },
    {
        "name": "missing_action_for_decision_request", "label_zh": "决策请求无操作建议",
        "label_tag": "决策请求无操作建议", "severity": "critical", "ceiling": 65,
        "description": "用户明确要求买卖建议但答案未给出。",
    },
    {
        "name": "missing_required_evidence", "label_zh": "遗漏必要证据",
        "label_tag": "遗漏必要证据", "severity": "warning", "ceiling": 60,
        "description": "推荐缺少必要的证据支撑。",
    },
    {
        "name": "overconfident_or_unsuitable_recommendation", "label_zh": "过度确定/不合适推荐",
        "label_tag": "过度确定/不合适推荐", "severity": "critical", "ceiling": 55,
        "description": "推荐过于确定或明显不适合用户画像。",
    },
    {
        "name": "template_generic_advice", "label_zh": "模板化通用建议",
        "label_tag": "模板化通用建议", "severity": "warning", "ceiling": 65,
        "description": "答案变成模板化通用建议，缺乏个性化。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {"l1": "intent", "l1_zh": "意图理解", "description": "误解推荐任务、未识别'适合我'、未区分买卖/持有/配置", "l2": ["recommendation_misjudged", "decision_type_missed"]},
    {"l1": "context", "l1_zh": "上下文使用", "description": "没有使用用户 KYC 数据、历史提问、持仓、偏好", "l2": ["kyc_not_used", "history_ignored", "profile_misapplied"]},
    {"l1": "evidence", "l1_zh": "证据支撑", "description": "关键数据缺失、证据浅、证据与推荐不匹配", "l2": ["insufficient_evidence", "shallow_evidence", "mismatched_evidence"]},
    {"l1": "tool", "l1_zh": "工具选择与执行", "description": "工具选择、输入、输出读取或效率问题", "l2": ["wrong_tool", "kyc_tool_not_called", "tool_output_misread"]},
    {"l1": "reasoning", "l1_zh": "推荐推理", "description": "推荐逻辑、适当性、仓位、触发条件推理失败", "l2": ["suitability_error", "position_logic_error", "trigger_misjudged"]},
    {"l1": "composition", "l1_zh": "答案组织", "description": "模板化、啰嗦、主结论不清、表达可信度差", "l2": ["template_output", "unclear_recommendation", "credibility_weak"]},
    {"l1": "safety_or_compliance", "l1_zh": "安全与合规", "description": "过度确定、风险边界缺失、不适当高风险推荐", "l2": ["overconfident", "missing_risk_boundary", "unsuitable_high_risk"]},
]

ROOT_CAUSE_DIM_MAP = {
    "intent_profile_understanding": "intent",
    "scenario_emotion_recognition": "intent",
    "suitability_personalization": "reasoning",
    "evidence_integration": "evidence",
    "decision_actionability": "reasoning",
    "risk_boundary_control": "safety_or_compliance",
    "composition_credibility": "composition",
    "tool_usage": "tool",
}


