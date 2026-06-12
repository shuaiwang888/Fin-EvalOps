# 04-分析评价类问题 Skill

> 自研模型「股票 / 基金 / 指数 / 宏观资产」分析评价类问题的评测协议，强调"**先识别评价需求，不先套题型**"。

---

## 一、Skill 定位与目标

**核心使命**：评测自研模型在**分析评价类**金融问答上的表现，**不先归入固定题型**，先判断本题要解决什么投资决策、需要什么证据、哪些评价维度决定答案质量。

**关键定位**：

- **主锚点**：`text_answer`
- **辅助证据**：`chain` + `online_dimension_signals`（线上失败样本、用户反馈）
- **设计哲学**：从**种子维度池**选维度，必要时**新增运行时维度**；主题（题材/基金/宏观/消息面）只作为检索专家案例的线索。

---

## 二、目录结构

```
04-分析评价类问题/
├── README.md
├── SKILL_zh.md
├── scripts/rule.py
└── references/
    ├── MANIFEST.md
    ├── output-schema_zh.md
    ├── rubric/                  # 10 种子维度 + 9 封顶
    │   ├── expert_answer_patterns.md  # 人工精标好/差答案模式
    │   └── [10 个维度文件]
    ├── golden_cases/            # 专家案例
    ├── root-cause/              # 5+1 个 L1（多了 capability_gap）
    └── tool_list/
```

---

## 三、适用范围

**适用**：

- 股票/指数/基金/ETF/宏观资产的分析、评价、诊断、趋势判断
- 行情归因：为什么上涨/没涨/冲高回落
- 决策类：能不能买、要不要切换、适不适合长期持有
- 个人化：适合我买什么、结合目标/风险/持仓/成本做推荐
- 业务类：消息面、题材发酵、客户占比、供应链、商业模式、估值逻辑

**不适用**：纯条件选股、纯行情查询、客服问题、图片搜索、不需要投资分析的简单事实查询。

**与 05 的边界**：混合了筛选、分析和推荐时，以"是否要求解释/判断/评价/个人化适配/决策支持"为准；若明显属于 KYC 推荐建议，优先用 05。

---

## 四、5 步执行协议

| 步骤 | 动作 | 关键产出 |
|---|---|---|
| **步骤 0** | **识别评价需求** + 抽维度 + 动态权重 | `weight_assignment`（总和=100） |
| **步骤 1** | 盲评最终答案 | 各维度 `raw_score` + `evidence` |
| **步骤 2** | 链路诊断 + 根因 + `tool_usage` 评分 | `root_causes` |
| **步骤 3** | 应用封顶规则 | `caps` 数组 |
| **步骤 4** | 序列化 JSON 输出 | 按 `output-schema_zh.md` |

**关键差异**：

- 必读 `expert_answer_patterns.md`（人工精标好/差答案模式）
- 允许**新增运行时维度**（`runtime_dimensions`），但必须用 `snake_case`、写清定义、不能与现有维度语义重复
- 若涉及"适合我"题，必须检查链路是否读取了用户画像/历史上下文

---

## 五、10 个种子维度（权重动态调整）

| 维度 | 建议权重 | 适用性 | 核心关注 |
|---|---:|---|---|
| `intent_scenario_recognition` 意图和场景识别 | 13 | **始终 relevant** | 用户真实任务、投资场景 |
| `evidence_source_quality` 证据来源质量 | 13 | relevant / supplementary | 搜索/研报/公告/调研/财务/行情 |
| `recency_time_boundary` 时效性和时间边界 | 8 | relevant / supplementary | 最新/最近/今天/消息面 |
| `investment_logic_depth` 投资逻辑深度 | 17 | **始终 relevant** | 核心投资逻辑、关键证据 |
| `method_fit` 分析方法匹配 | 10 | **始终 relevant** | 题型/标的/周期匹配 |
| `comparison_quantification` 对比和量化 | 8 | relevant / supplementary | 基金/估值/指数/对比/排序 |
| `actionability_risk` 可执行性和风险 | 8 | relevant / supplementary | 能不能买/持有/切换/配置 |
| `user_profile_suitability` 用户画像适配 | 8 | relevant / supplementary / NA | "适合我"/结合目标/风险/持仓 |
| `scenario_emotion_recognition` 场景与情绪识别 | 4 | relevant / supplementary / NA | 浮亏/套牢/迷茫/急于回本 |
| `composition_credibility` 表达可信度 | 5 | **始终 supplementary** | |
| `tool_usage` 工具使用合理性 | 6 | **始终 relevant**（链路诊断） | |

**可新增运行时维度示例**：

- `business_purity` 题材业务与主题真实相关度
- `holding_style_fit` 持仓风格与用户偏好匹配
- `event_materiality` 消息面实质影响区分
- `product_universe_fit` ETF/基金/组合产品池
- `recommendation_consistency` 同一画像下推荐稳定性
- `stock_style_logic_fit` 个股分析识别游资/题材/机构等不同交易逻辑
- `source_depth_fit` 资料深度（调研纪要/研报全文）

---

## 六、9 个封顶规则（cap rules）

| 规则 | 上限 | 触发场景 |
|---|---:|---|
| `missed_core_investment_logic` 缺失核心投资逻辑 | **60** | 没抓到真实投资逻辑 |
| `stale_or_wrong_time_evidence` 旧消息/时间边界错误 | **50** | 旧数据/旧公告冒充最新 |
| `method_mismatch` 分析方法明显错位 | **55** | 方法不适合题型/标的/周期 |
| `template_data_dump` 模板化数据堆砌 | **60** | 四大面套模板 |
| `missing_required_analysis_elements` 题型必需分析要素缺失 | **65** | 关键要素全无 |
| `wrong_or_shallow_source` 证据来源类型错误/过浅 | **55** | 应该查调研纪要但只查了新闻 |
| `missing_user_profile_fit` 个人化建议缺少画像适配 | **60** | 适合我题未考虑用户画像 |
| `misread_loss_or_emotion_context` 误读亏损/迷茫/套牢场景 | **50** | 浮亏场景给短线抓反弹 |
| `overconfident_or_unsuitable_action` 过度确定/不适当行动 | **55** | 装确定给高波动推荐 |
| `missing_decision_action_for_recommendation` 推荐/交易请求缺行动输出 | **65** | 问能不能买但不给可执行建议 |

---

## 七、6 个 L1 根因归因体系

| L1 | 核心问题 |
|---|---|
| `intent` 理解问题 | 意图理解、画像/上下文处理 |
| `evidence` 检索证据 | 证据来源、深度、覆盖、时效 |
| `tool` 选择与执行工具 | 工具选择、参数、误读结果 |
| `reasoning` 计算与推理 | 投资逻辑、计算、对比 |
| `composition` 组织答案 | 表达可信度、非模板化 |
| `capability_gap` **能力/数据源缺口** | 工具能力/数据源本身缺失 |

`capability_gap` 是本 skill 独有的 L1 阶段——专门标记"工具能力/数据源本身缺失"类问题。

---

## 八、关键评分原则（保守评分 7 条）

1. **最终答案决定用户侧质量**，链路只用于归因
2. **不要把"有表格/有指标/有工具调用"自动视为高质量**
3. **投资分析类问题优先评估是否抓住核心投资逻辑、关键证据、时间边界、可执行判断**
4. **先判断答案是否贴近用户真实交易心理** —— 消息面/题材问题看能否帮用户理解当下能不能赚钱、逻辑是否变了、资金为什么选/不选
5. **涉及个人化推荐时，先评估是否理解"人"和"处境"**，再评估标的逻辑
6. **对浮亏/腰斩/迷茫场景** —— 优先检查是否先降风险、稳住决策框架、给仓位/复盘/证伪条件；直接推荐短线/抓反弹/高波动主题应重扣
7. **对模板化、数据堆砌、技术指标错用、旧消息冒充最新消息保持严格扣分**

---

## 九、必读 `expert_answer_patterns.md`

这个文件是 04 特有的——从人工精标截图中提炼的**好答案/差答案模式**和**场景化评判锚点**。特别用于校准：

- 低密度长答案
- 方法错位
- 表面资讯拼接
- 模板化回答

---

## 十、工具与输出

工具复用 01 的工具集：`Search` / `FinQuery` / `AccessingFullText` / `CodeInterpreter`

JSON 输出同 01 模式。**特别字段**：`runtime_dimensions`（当新增临时维度时使用）。

---

## 十一、与其他 skill 的边界

- ❌ **不适用**：纯条件选股、纯行情查询、客服问题、图片搜索、简单事实查询
- 与 **05-KYC 推荐建议**：用户画像/适配是核心时优先用 05
- 与 **03-诊股查数**：本 skill 偏评价/分析，03 偏取数诊断
- 与 **01-事件与概念选股**：本 skill 偏分析评价，01 偏排序选股

---

## 快速上手 Checklist

1. **步骤 0** 先通读 `expert_answer_patterns.md`（**必读**）+ `rubric/_index.md` + 必要 L1 文件
2. **步骤 1** 评估是否抓住核心投资逻辑（17 分大权重）
3. **步骤 2** 检查是否理解"人"和"处境"（浮亏/迷茫/套牢题）
4. **步骤 3** 检查 10 个封顶规则（多个，**特别注意 user_profile_fit**）
5. **步骤 4** 输出 JSON，可附 `runtime_dimensions`

**核心方法论**：「**先识别评价需求，再选维度，不先套题型**；投资逻辑深度（17）永远是核心。」
