"""
05-kyc-recommendation-suggestions result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义 KYC 推荐建议类金融问答的最终回答质量维度、默认权重和质量标签。
pairwise 比较字段由输出 schema 约束。
"""

DIMENSIONS = [
    {
        "key": "intent_profile_understanding",
        "label_zh": "意图与画像理解",
        "description": "评估最终回答是否准确理解用户推荐/决策目标，并处理用户问题中明示的个人化约束或画像不足。",
        "six_level_anchors": {
            0: "完全未理解用户推荐或投资决策目标",
            20: "只做泛泛推荐，与用户问题中的个人化约束几乎无关",
            40: "部分触及意图，但遗漏关键的风险、期限、资金、持仓、目标或画像不足",
            60: "基本理解意图和个人化约束，但个别关键约束利用不足",
            80: "准确理解推荐目标和个人化约束，回答与用户处境高度匹配",
            100: "完美理解显性和隐性推荐目标，画像约束、未知信息和推荐路径处理精准",
        },
    },
    {
        "key": "scenario_emotion_recognition",
        "label_zh": "场景与情绪识别",
        "description": "评估最终回答是否识别用户亏损、套牢、迷茫、焦虑或急于回本等真实投资处境。",
        "six_level_anchors": {
            0: "完全误读用户处境，并诱导继续高风险操作",
            20: "察觉少量情绪信号，但仍按普通推荐或短线机会处理",
            40: "能看出用户处境，但缺少降风险、复盘和纪律框架",
            60: "基本识别用户处境，并给出部分风险控制建议",
            80: "准确识别情绪和投资状态，能转化为稳健行动框架",
            100: "完美识别用户处境，先稳定决策纪律，再给分层动作和风险边界",
        },
    },
    {
        "key": "suitability_personalization",
        "label_zh": "适当性与个性化",
        "description": "评估最终回答的推荐是否匹配用户问题中明示的风险偏好、投资期限、资金目标、持仓背景和波动承受能力。",
        "six_level_anchors": {
            0: "推荐完全不适合用户问题中的约束，风险等级或期限明显冲突",
            20: "推荐方向与用户明示画像存在重大偏差",
            40: "推荐大致方向可行，但缺少对关键个人约束的考量",
            60: "推荐基本适合用户，但个性化程度不够或风险匹配不够精细",
            80: "推荐高度个性化，与用户风险、期限、目标和处境匹配",
            100: "推荐完美适配，每个建议都有明确适配理由和边界",
        },
    },
    {
        "key": "evidence_integration",
        "label_zh": "多维证据整合",
        "description": "评估最终回答是否整合与推荐相关的市场、宏观、行业、估值、技术、资金、产品或历史阶段证据。",
        "six_level_anchors": {
            0: "完全没有证据支撑，纯主观推荐",
            20: "仅有一两个泛泛证据点，不足以支撑推荐结论",
            40: "有一定证据但维度单一，缺少关键比较或交叉验证",
            60: "多维证据基本具备，但证据与推荐动作的关联不够紧密",
            80: "多维证据充分整合，相互印证并支撑推荐逻辑",
            100: "证据整合完美，多维数据、同类比较和历史验证形成完整推荐依据",
        },
    },
    {
        "key": "decision_actionability",
        "label_zh": "决策可执行性",
        "description": "评估最终回答是否给出可执行的买卖、持有、加仓、减仓、配置、仓位、触发条件或下一步动作。",
        "six_level_anchors": {
            0: "完全没有可执行建议",
            20: "只有方向性建议，没有操作细节",
            40: "有操作建议，但缺少关键仓位、时机、触发条件或优先级",
            60: "操作建议基本可执行，但个别边界或条件不够明确",
            80: "操作建议清晰可执行，仓位、时机、条件和备选方案明确",
            100: "行动方案完美，每一步都有条件、仓位、证伪和备选路径",
        },
    },
    {
        "key": "risk_boundary_control",
        "label_zh": "风险控制与边界",
        "description": "评估最终回答是否给出风险边界、止损止盈、仓位上限、证伪条件和不确定性表达。",
        "six_level_anchors": {
            0: "完全没有风险提示或边界控制",
            20: "有风险提及但流于形式，没有实质性风控措施",
            40: "有风控方向但缺少具体阈值、止损或证伪条件",
            60: "风险边界基本清晰，但极端情景或集中暴露未充分警示",
            80: "风险边界明确，止损、仓位和证伪条件具体可执行",
            100: "风控完美，多情景压力测试、仓位管理和退出条件完整",
        },
    },
    {
        "key": "product_universe_fit",
        "label_zh": "产品池与配置角色适配",
        "description": "评估最终回答的基金、ETF、股票或资产候选池是否合理，并说明其配置角色。",
        "six_level_anchors": {
            0: "产品池完全不适合用户任务，或高风险集中暴露与问题约束冲突",
            20: "候选池明显偏窄、偏热门或缺少基本适配理由",
            40: "产品池部分可用，但缺少配置角色、优先级或同类比较",
            60: "产品池基本合理，但核心/卫星、防守/进攻角色不够清楚",
            80: "产品池合理，配置角色、互补关系、风险收益边界清楚",
            100: "产品池完美，候选、配置角色、费率/流动性/回撤/替代比较完整",
        },
    },
    {
        "key": "recommendation_stability",
        "label_zh": "推荐稳定性与变化解释",
        "description": "评估最终回答是否呈现稳定推荐原则，并在推荐变化或一致性诉求下给出清楚解释。",
        "six_level_anchors": {
            0: "推荐口径完全随机或自相矛盾",
            20: "有少量原则但推荐变化缺乏解释",
            40: "筛选原则不够稳定，变化理由含糊",
            60: "基本有稳定原则，但对变化原因或适用条件解释不足",
            80: "推荐原则稳定，变化来自市场、目标、风险或产品数据并解释清楚",
            100: "推荐体系高度稳定，可延续、可复核，并能清楚处理变化情形",
        },
    },
    {
        "key": "composition_credibility",
        "label_zh": "表达可信度",
        "description": "评估最终回答表达是否清楚、审慎、可信、非模板化。",
        "six_level_anchors": {
            0: "表达完全不可信，包含严重误导信息",
            20: "表达模糊空洞，大量无根据断言",
            40: "有可信内容但掺杂主观臆断或模板化套话",
            60: "表达基本可信审慎，但主结论或边界仍不够清楚",
            80: "表达可信、客观、审慎，结论、依据、动作和风险清楚",
            100: "表达完美，每项结论有证据，结构清晰，无夸大和模板化",
        },
    },
]

DEFAULT_WEIGHTS = {
    "intent_profile_understanding": 17,
    "scenario_emotion_recognition": 9,
    "suitability_personalization": 17,
    "evidence_integration": 13,
    "decision_actionability": 15,
    "risk_boundary_control": 12,
    "product_universe_fit": 7,
    "recommendation_stability": 5,
    "composition_credibility": 5,
}

WEIGHT_RULES: list[dict] = []

CAP_RULES = [
    {
        "name": "missing_kyc_profile",
        "label_zh": "个人化建议缺少画像适配",
        "label_tag": "个人化建议缺少画像适配",
        "severity": "critical",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "用户要求个人化推荐或结合自身情况决策，但最终回答没有体现用户问题中明示的风险、期限、目标、资金、持仓或画像不足。",
    },
    {
        "name": "misread_emotional_loss_context",
        "label_zh": "误读亏损/情绪场景",
        "label_tag": "误读亏损/情绪场景",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答误读用户亏损、套牢、迷茫、焦虑或急于回本处境，把风险控制问题当成普通推荐入口。",
    },
    {
        "name": "fabricated_user_profile",
        "label_zh": "虚构用户画像",
        "label_tag": "虚构用户画像",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答使用了用户问题中不存在、无法支持或明显编造的风险等级、资金规模、期限、风格、持仓或偏好。",
    },
    {
        "name": "missing_action_for_decision_request",
        "label_zh": "决策请求无操作建议",
        "label_tag": "决策请求无操作建议",
        "severity": "critical",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "用户要求买卖、持有、加仓、减仓、配置或推荐，但最终回答没有给出可执行动作、触发条件或下一步。",
    },
    {
        "name": "missing_required_evidence",
        "label_zh": "遗漏必要证据",
        "label_tag": "遗漏必要证据",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答的推荐缺少问题所需的关键证据、同类比较、历史位置、估值、回撤、产品或市场依据。",
    },
    {
        "name": "overconfident_or_unsuitable_recommendation",
        "label_zh": "过度确定/不合适推荐",
        "label_tag": "过度确定/不合适推荐",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答给出过度确定或明显不适合用户场景的推荐，可能诱导用户承担与问题约束不匹配的风险。",
    },
    {
        "name": "template_generic_advice",
        "label_zh": "模板化通用建议",
        "label_tag": "模板化通用建议",
        "severity": "warning",
        "ceiling": 65,
        "score_effect": "tag_only",
        "description": "最终回答变成模板化通用建议，缺少对用户问题和推荐目标的具体响应。",
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
