# 12-金融逻辑推理 Skill

> 自研模型「投资判断、走势预测、个股选择、强势股筛选、板块内比较和风险情景推演」类问题的评测协议。

---

## 一、Skill 定位与目标

**核心使命**：评测问财模型是否能把**金融事实、市场驱动、个股属性、资金/技术/基本面证据**推导成**有决策价值的结论**。

**关键定位**：

- **主锚点**：`text_answer`
- **辅助证据**：`chain`（只用于工具使用和根因归因）
- **设计哲学**：从题目识别**预测、筛选、比较、排序、操作建议还是风险推演**，再判断证据是否真的支持结论，而不是只堆技术面、资金面或公告。

---

## 二、目录结构

```
12-金融逻辑推理/
├── README.md
├── SKILL_zh.md
├── scripts/rule.py
└── references/
    ├── MANIFEST.md
    ├── output-schema_zh.md
    ├── output-schema_round1_zh.md
    ├── rubric/         # 7 维度 + 6 封顶
    ├── golden_cases/   # 专家文本案例 + image_annotation_anchors
    ├── root-cause/     # 5 个 L1
    └── tool_list/
```

---

## 三、适用范围

**适用**：

- 便宜有潜力的股票、明天可能涨停的股票
- 个股下周走势、还能不能追、后市怎么操作
- 多只概念股怎么选、谁弹性更强、谁更稳健
- 根据市场热点、资金、技术面、基本面和事件催化形成投资逻辑

**不适用**：

- 只考察单个金融术语定义（用 10）
- 单纯指令未遵循（用 11）

---

## 四、5 步执行协议

| 步骤 | 动作 | 关键产出 |
|---|---|---|
| **步骤 0** | **识别决策任务** + 适用性 + 动态权重 | `weight_assignment`（总和=100） |
| **步骤 1** | **盲评推理质量** | 各维度 `raw_score` + `evidence` |
| **步骤 2** | 链路诊断 + 根因 + `tool_usage` 评分 | `root_causes` |
| **步骤 3** | 应用封顶规则 | `caps` 数组 |
| **步骤 4** | 序列化 JSON 输出 | 按 `output-schema_zh.md` |

**关键步骤强调**：

- **步骤 0**：判断题目需要**预测、筛选、比较、排序、操作建议还是风险推演**
- **步骤 1**：判断**证据是否真的支持结论**，而不是只堆技术面、资金面或公告

---

## 五、7 个评分维度

| 维度 | 建议权重 | 适用性 | 核心关注 |
|---|---:|---|---|
| `financial_logic_chain` 金融逻辑链完整性 | 25 | **始终 relevant** | 是否形成从事实到结论的闭环（**最高权重**） |
| `market_driver_identification` 市场驱动识别 | 20 | relevant / supplementary | 短线/热点/走势/板块题 |
| `evidence_to_conclusion` 证据到结论连接 | 20 | **始终 relevant** | 数据/新闻/公告/资金是否支撑结论 |
| `comparison_and_ranking` 个股比较与排序 | 15 | relevant / supplementary | 多股选择/怎么选/推荐/排序 |
| `scenario_risk_reasoning` 情景与风险推演 | 10 | relevant | 预测/追高/操作建议/下周/明天题 |
| `decision_value_expression` 决策价值表达 | 5 | **始终 supplementary** | 操作建议题 relevant |
| `tool_usage` 工具使用合理性 | 5 | **始终 relevant** | |

**权重动态调整**：

- 预测/操作建议题 → 提高 `scenario_risk_reasoning` 和 `decision_value_expression`
- 多股比较题 → 提高 `comparison_and_ranking`
- 热点短线题 → 提高 `market_driver_identification`
- 纯基本面价值题 → 提高 `financial_logic_chain` 和 `evidence_to_conclusion`

---

## 六、6 个封顶规则（cap rules）

| 规则 | 上限 | 触发场景 |
|---|---:|---|
| `unsupported_prediction_or_recommendation` 无支撑预测/推荐 | **45** | 装确定给涨停/收益判断 |
| `wrong_core_investment_logic` 核心投资逻辑错误 | **50** | 逻辑链方向错 |
| `market_driver_missing` 市场驱动缺失 | **55** | 短线题忽略热点和题材情绪 |
| `data_dump_without_reasoning` 数据堆砌无推导 | **55** | 只堆指标没逻辑 |
| `comparison_without_standard` 比较无统一标准 | **60** | 多股比较没统一比较维度 |
| `risk_scenario_missing_for_high_risk_advice` 高风险建议缺风险情景 | **65** | 高波动操作建议没给风险情景 |

---

## 七、5 个 L1 根因归因体系

标准 5 个 L1：`intent` / `evidence` / `tool` / `reasoning` / `composition`

`reasoning` 在本 skill 中特指**投资逻辑推导根因**。

---

## 八、关键评分原则（安全护栏 6 条）

1. **不要把单一指标当成完整投资逻辑** —— 估值/资金/技术面/公告都需要解释"为什么影响未来"
2. **"便宜"不等于 PE 为负**；"有潜力"需要增长/景气/催化/资金逻辑
3. **预测类问题要给情景、条件和风险**，不得保证涨停或确定收益
4. **多股比较要有统一标准** —— 业务占比、弹性、自给率、资金承接、估值、安全边际
5. **不能用八股文四大面堆砌替代重点分析**
6. **对短线题，市场热点和题材发酵链路往往比静态指标更关键**

---

## 九、常见失败（5 条）

- 便宜有潜力只看估值，甚至选 PE 为负
- 明天涨停只看连板，不找市场热点和题材情绪
- 个股走势只解读单个常规公告，忽略前期上涨原因、资金流和机构行为
- 后市分析用"四大面"模板堆指标，缺少重点
- 多股怎么选只看技术面，不比较业务占比、弹性、自给率和风险

---

## 十、JSON 输出契约

**schema_version**：`financial-logical-reasoning/v1`

---

## 十一、与其他 skill 的边界

- ❌ **不适用**：只考察单个金融术语定义、单纯指令未遵循
- 与 **10-金融常识与语义理解**：本 skill 偏动态逻辑推演；10 偏静态概念
- 与 **11-指令遵循能力**：本 skill 偏投资逻辑；11 偏主指令完成
- 与 **04-分析评价类问题**：本 skill 偏推理；04 偏评价
- 与 **02-回测取数计算**：本 skill 偏推理结论；02 偏取数计算

---

## 快速上手 Checklist

1. **步骤 0** **识别决策任务类型**（预测/筛选/比较/排序/操作/风险推演）
2. **步骤 1** 重点检查**金融逻辑链（25）**+**市场驱动（20）**+**证据到结论（20）**三大权重
3. **步骤 2** 检查推理链完整性
4. **步骤 3** 检查 6 个封顶（**特别注意 `wrong_core_investment_logic` 上限 50 和 `risk_scenario_missing_for_high_risk_advice` 上限 65**）
5. **步骤 4** 输出 JSON

**核心方法论**：「**金融逻辑链（25）**是核心；证据真的支持结论，而不是堆指标。」
