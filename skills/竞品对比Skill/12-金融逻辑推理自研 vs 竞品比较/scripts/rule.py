"""
12-financial-logical-reasoning-self-vs-competitor 评测规则定义。

该比较 skill 沿用第 12 类金融逻辑推理的绝对评分维度、默认权重、
封顶规则和根因体系；pairwise 比较字段由输出 schema 约束。
"""

# 维度定义

DIMENSIONS = [
    {
        "key": "financial_logic_chain",
        "label_zh": "金融逻辑链",
        "description": "判断答案是否把金融事实、市场驱动、个股属性、资金/技术/基本面证据推导成完整投资逻辑。",
        "score_anchors": {
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
        "description": "判断答案是否识别热点、催化、资金、技术、基本面或价格驱动。",
        "score_anchors": {
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
        "description": "判断证据是否真正支撑预测、筛选、排序、建议或风险判断。",
        "score_anchors": {
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
        "description": "判断多股比较、筛选和排序是否有统一标准并形成优先级。",
        "score_anchors": {
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
        "description": "判断预测或操作建议是否给出情景、条件和风险边界。",
        "score_anchors": {
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
        "description": "判断答案是否清楚表达用户可用的选择、排序、建议、条件或下一步动作。",
        "score_anchors": {
            0: "没有可用结论",
            20: "结论被数据或背景淹没，用户无法行动",
            40: "有笼统结论但缺少条件或优先级",
            60: "基本可用，但表达不够聚焦或边界不足",
            80: "结论清楚，有较好决策价值",
            100: "先结论后逻辑，优先级、条件、风险和行动建议清晰可用",
        },
    },
    {
        "key": "tool_usage",
        "label_zh": "工具使用合理性",
        "description": "判断工具选择、查询设计、交叉验证和工具结果转化是否合理。",
        "score_anchors": {
            0: "需要工具但完全未使用，或工具调用全错",
            20: "工具选择明显错误，关键证据缺失",
            40: "使用了相关工具但参数、时点或覆盖不足",
            60: "工具基本合理，但交叉验证或结果转化不足",
            80: "工具选择和调用较好，少量冗余或遗漏",
            100: "工具组合精准高效，证据覆盖充分并成功转化成答案质量",
        },
    },
]

# 默认权重与第 12 类自研 skill 输出 schema 示例保持一致，sum=100。

DEFAULT_WEIGHTS = {
    "financial_logic_chain": 25,
    "market_driver_identification": 20,
    "evidence_to_conclusion": 20,
    "comparison_and_ranking": 15,
    "scenario_risk_reasoning": 10,
    "decision_value_expression": 5,
    "tool_usage": 5,
}

CAP_RULES = [
    {
        "name": "unsupported_prediction_or_recommendation",
        "label_zh": "无支撑预测或推荐",
        "severity": "critical",
        "ceiling": 45,
        "description": "给出明确预测、推荐、买卖或追涨建议，但缺少支撑证据、条件边界或风险说明。",
    },
    {
        "name": "evidence_conclusion_disconnect",
        "label_zh": "结论与证据脱节",
        "severity": "critical",
        "ceiling": 50,
        "description": "数据、公告、技术面或资金信息不能支撑最终结论。",
    },
    {
        "name": "missing_key_market_driver",
        "label_zh": "关键市场驱动缺失",
        "severity": "critical",
        "ceiling": 55,
        "description": "题目核心依赖热点、催化、资金、技术、基本面或行业景气，但答案遗漏关键驱动。",
    },
    {
        "name": "overconfident_risk_commitment",
        "label_zh": "收益/风险承诺过度",
        "severity": "critical",
        "ceiling": 45,
        "description": "对涨停、上涨、收益或买卖时点作出确定性承诺，忽略风险和不成立条件。",
    },
    {
        "name": "comparison_logic_error",
        "label_zh": "比较或排序逻辑错误",
        "severity": "warning",
        "ceiling": 60,
        "description": "比较标准混乱、口径不一致，或排序理由与排序结果矛盾。",
    },
    {
        "name": "data_dump_without_reasoning",
        "label_zh": "数据堆砌替代推理",
        "severity": "warning",
        "ceiling": 55,
        "description": "主要输出列表、表格、指标或公告摘要，缺少证据如何支撑结论的解释。",
    },
]

ROOT_CAUSE_TAXONOMY = [
    {
        "l1": "intent",
        "l1_zh": "理解决策任务",
        "description": "是否识别用户要做预测、筛选、比较、排序、操作建议或风险推演。",
        "l2": [
            "decision-task-misread",
            "decision-object-misread",
            "time-horizon-missed",
            "comparison-intent-missed",
            "risk-intent-missed",
        ],
    },
    {
        "l1": "evidence",
        "l1_zh": "收集证据",
        "description": "证据是否覆盖市场驱动、个股属性、时效和风险条件。",
        "l2": [
            "market-driver-evidence-missing",
            "stock-attribute-evidence-missing",
            "stale-or-wrong-evidence",
            "single-indicator-overused",
            "conflicting-evidence-unresolved",
            "risk-evidence-missing",
        ],
    },
    {
        "l1": "tool",
        "l1_zh": "工具策略",
        "description": "工具是否选对、用对，并完成必要交叉验证。",
        "l2": [
            "wrong-tool-selection",
            "wrong-tool-params",
            "missing-realtime-or-structured-check",
            "missing-cross-validation",
            "tool-output-not-transformed",
            "over-fetching-no-synthesis",
        ],
    },
    {
        "l1": "reasoning",
        "l1_zh": "投资逻辑推导",
        "description": "是否把证据推导成有决策价值的金融结论。",
        "l2": [
            "broken-investment-logic-chain",
            "market-driver-missed",
            "evidence-conclusion-disconnect",
            "comparison-standard-missing",
            "scenario-risk-missing",
            "overconfident-inference",
            "single-factor-reasoning",
            "static-data-over-dynamic-market",
        ],
    },
    {
        "l1": "composition",
        "l1_zh": "组织答案",
        "description": "是否把逻辑清楚呈现成用户可用的判断。",
        "l2": [
            "data-dump-no-synthesis",
            "conclusion-not-actionable",
            "risk-boundary-not-presented",
            "ranking-presentation-unclear",
            "generic-template",
            "key-judgment-buried",
        ],
    },
]

ROOT_CAUSE_DIM_MAP = {
    "financial_logic_chain": "reasoning",
    "market_driver_identification": "reasoning",
    "evidence_to_conclusion": "reasoning",
    "comparison_and_ranking": "reasoning",
    "scenario_risk_reasoning": "reasoning",
    "decision_value_expression": "composition",
    "tool_usage": "tool",
}
