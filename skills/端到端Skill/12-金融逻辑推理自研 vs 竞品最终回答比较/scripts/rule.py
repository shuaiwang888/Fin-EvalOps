"""
12-financial-logical-reasoning result-only 自研 vs 竞品评测规则定义。

该比较 skill 只定义金融逻辑推理领域的最终回答质量维度、默认权重和封顶标签。
pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "financial_logic_chain",
        "label_zh": "金融逻辑链",
        "description": "评估最终回答是否把金融事实、市场驱动、个股属性、资金/技术/基本面证据推导成完整投资逻辑。",
        "six_level_anchors": {
            0: "完全没有金融逻辑或对象错误",
            20: "仅有零散指标、行情或概念，无法形成推理链",
            40: "有部分相关逻辑，但关键传导环节明显断裂",
            60: "方向基本正确，但逻辑链不够完整或个股落点偏弱",
            80: "逻辑链基本完整，少量条件、风险或证据细节不足",
            100: "事实、驱动、证据、结论完整闭环，具备高质量决策价值",
        },
    },
    {
        "key": "market_driver_identification",
        "label_zh": "市场驱动识别",
        "description": "评估最终回答是否识别热点、催化、资金、技术、基本面或价格驱动。",
        "six_level_anchors": {
            0: "完全没有识别市场驱动",
            20: "只复述涨跌或概念标签",
            40: "提到部分驱动但主次混乱或遗漏关键因素",
            60: "主要驱动方向正确，但缺少时效、传导或持续性判断",
            80: "驱动识别清晰，只有轻微遗漏",
            100: "准确识别并分层解释核心驱动、次要驱动和持续性",
        },
    },
    {
        "key": "evidence_to_conclusion",
        "label_zh": "证据到结论",
        "description": "评估最终回答中的证据是否真正支撑预测、筛选、排序、建议或风险判断。",
        "six_level_anchors": {
            0: "结论无证据或捏造证据",
            20: "证据与结论基本脱节",
            40: "证据只能支撑部分结论，关键判断缺乏支撑",
            60: "证据大体相关，但解释和交叉验证不足",
            80: "证据基本支撑结论，少量反证或边界未展开",
            100: "关键结论均有匹配证据，证据链可复核且边界清晰",
        },
    },
    {
        "key": "comparison_and_ranking",
        "label_zh": "比较与排序",
        "description": "评估最终回答中的多股比较、筛选和排序是否有统一标准并形成优先级。",
        "six_level_anchors": {
            0: "用户需要比较或排序但完全未提供",
            20: "只有名单或分别介绍，没有比较标准",
            40: "有比较意图但标准混乱或口径不一致",
            60: "排序方向基本合理，但理由不够充分",
            80: "比较标准清楚，排序基本有据",
            100: "统一标准、证据和风险边界共同支撑排序，决策价值高",
        },
    },
    {
        "key": "scenario_risk_reasoning",
        "label_zh": "情景与风险推理",
        "description": "评估最终回答中的预测或操作建议是否给出情景、条件和风险边界。",
        "six_level_anchors": {
            0: "给出确定性收益/涨停/买卖承诺或完全无风险意识",
            20: "风险提示模板化，不能约束结论",
            40: "有风险意识但缺少情景和不成立条件",
            60: "给出基本风险和条件，但与结论结合不紧",
            80: "情景、条件和风险较完整，少量细节不足",
            100: "多情景推理清晰，结论、触发条件和失效条件完整闭环",
        },
    },
    {
        "key": "decision_value_expression",
        "label_zh": "决策价值表达",
        "description": "评估最终回答是否清楚表达用户可用的选择、排序、建议、条件或下一步动作。",
        "six_level_anchors": {
            0: "没有可用结论",
            20: "结论被数据或背景淹没，用户无法行动",
            40: "有笼统结论但缺少条件或优先级",
            60: "基本可用，但表达不够聚焦或边界不足",
            80: "结论清楚，有较好决策价值",
            100: "先结论后逻辑，优先级、条件、风险和行动建议清晰可用",
        },
    },
]

# 默认权重（总和 100），LLM 动态权重回退时使用。
# 原过程相关权重已并入可从最终回答判断的证据到结论维度。

DEFAULT_WEIGHTS = {
    "financial_logic_chain": 25,
    "market_driver_identification": 20,
    "evidence_to_conclusion": 25,
    "comparison_and_ranking": 15,
    "scenario_risk_reasoning": 10,
    "decision_value_expression": 5,
}

WEIGHT_RULES: list[dict] = []

# 封顶标签（保留原类别标签语义，不直接修改分数）

CAP_RULES = [
    {
        "name": "unsupported_prediction_or_recommendation",
        "label_zh": "无支撑预测或推荐",
        "label_tag": "无支撑预测/推荐",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答给出明确预测、推荐、买卖或追涨建议，但缺少支撑证据、条件边界或风险说明。",
    },
    {
        "name": "evidence_conclusion_disconnect",
        "label_zh": "结论与证据脱节",
        "label_tag": "结论与证据脱节",
        "severity": "critical",
        "ceiling": 50,
        "score_effect": "tag_only",
        "description": "最终回答中的数据、公告、技术面或资金信息不能支撑最终结论。",
    },
    {
        "name": "missing_key_market_driver",
        "label_zh": "关键市场驱动缺失",
        "label_tag": "关键市场驱动缺失",
        "severity": "critical",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "题目核心依赖热点、催化、资金、技术、基本面或行业景气，但最终回答遗漏关键驱动。",
    },
    {
        "name": "overconfident_risk_commitment",
        "label_zh": "收益/风险承诺过度",
        "label_tag": "收益/风险承诺过度",
        "severity": "critical",
        "ceiling": 45,
        "score_effect": "tag_only",
        "description": "最终回答对涨停、上涨、收益或买卖时点作出确定性承诺，忽略风险和不成立条件。",
    },
    {
        "name": "comparison_logic_error",
        "label_zh": "比较或排序逻辑错误",
        "label_tag": "比较/排序逻辑错误",
        "severity": "warning",
        "ceiling": 60,
        "score_effect": "tag_only",
        "description": "最终回答中的比较标准混乱、口径不一致，或排序理由与排序结果矛盾。",
    },
    {
        "name": "data_dump_without_reasoning",
        "label_zh": "数据堆砌替代推理",
        "label_tag": "数据堆砌替代推理",
        "severity": "warning",
        "ceiling": 55,
        "score_effect": "tag_only",
        "description": "最终回答主要输出列表、表格、指标或公告摘要，缺少证据如何支撑结论的解释。",
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
