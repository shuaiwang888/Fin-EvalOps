# 05-KYC推荐建议类问题 Skill

> 自研模型「投资推荐、配置建议、交易决策支持」类问题的评测协议，**默认强 KYC 标准**：模型应主动使用用户 KYC 数据进行回答。

---

## 一、Skill 定位与目标

**核心使命**：评测自研模型在 **KYC 推荐建议类**金融问题上的表现。

**关键定位**：

- **主锚点**：`text_answer`
- **关键输入**：`meta.user_investment_goal`（用户风险承受能力、投资目标、投资周期、分析方法、投资理念等）
- **强 KYC 标准**：只要问题属于投资推荐/配置建议/交易决策支持，就应检查模型**是否主动获取并使用用户 KYC 数据**。若没有使用，应评测出"理当使用 KYC，但实际未使用"的问题点。
- **设计哲学**：05 类问题最重要的质量标准是**"私人投顾感"** —— 让用户看出模型知道我是谁、我处在什么投资状态、为什么这个建议适合我。

---

## 二、目录结构

```
05-KYC推荐建议类问题/
├── README.md
├── SKILL_zh.md
├── scripts/rule.py
└── references/
    ├── MANIFEST.md
    ├── output-schema_zh.md  # schema_version: kyc-recommendation-suggestions/v1
    ├── rubric/              # 10 维度 + 7 封顶
    ├── golden_cases/        # 13 个专家案例 + image_annotation_anchors
    ├── root-cause/          # 6 个 L1（多了 context 和 safety_or_compliance）
    └── tool_list/           # 工具直接复用 01
```

---

## 三、适用范围

**适用**：

- 推荐适合我的股票/基金/ETF/行业/资产/组合
- 能不能买、是否继续持有、该割肉还是加仓、怎么控制仓位
- 结合我的目标/风险/资金/持仓/风格给建议
- 宏观/行业/市场情景下的方向选择、资产比较、配置顺序
- 用户处于浮亏/套牢/迷茫/信心受挫等真实投资处境时的投顾式建议

**不适用**：纯行情查询、纯事实查询、客服问题、图片搜索、不需要用户适配的普通资料总结。

**边界判定**：同时包含分析和推荐时，以**是否需要给用户做适配后的决策建议**为准。

---

## 四、5 步执行协议

| 步骤 | 动作 | 关键产出 |
|---|---|---|
| **步骤 0** | **识别推荐场景** + 抽维度 + 动态权重 | `weight_assignment`（总和=100） |
| **步骤 1** | 盲评最终答案 + **对照 `meta.user_investment_goal`** | 各维度 `raw_score` + `evidence` |
| **步骤 2** | 链路诊断 + 根因 + `tool_usage` 评分 | `root_causes`（**重点检查 KYC 使用**） |
| **步骤 3** | 应用封顶规则 | `caps` 数组 |
| **步骤 4** | 序列化 JSON 输出 | 按 `output-schema_zh.md` |

**关键步骤强调**：

- **步骤 1**：若提供了 `meta.user_investment_goal`，必须将答案与该画像对照；不匹配的推荐（如向保守型用户推荐高波动标的）应在画像理解、适当性等维度扣分
- **步骤 2**：必须专门检查链路是否有**读取、调用、检索或引用用户 KYC 数据**的动作
- **新增运行时维度**与 04 类似

---

## 五、10 个评分维度（权重动态调整）

| 维度 | 建议权重 | 适用性 | 核心关注 |
|---|---:|---|---|
| `intent_profile_understanding` 意图与画像理解 | 18 | **始终 relevant** | 用户意图 + 画像理解 |
| `scenario_emotion_recognition` 场景与情绪识别 | 10 | relevant / supplementary | 亏损/套牢/迷茫/急于回本/私人投顾感 |
| `suitability_personalization` 适当性与个性化 | 18 | **始终 relevant** | 推荐是否适合用户画像 |
| `evidence_integration` 多维证据整合 | 14 | relevant / supplementary | 市场/宏观/行业/估值/技术/资金/历史阶段 |
| `decision_actionability` 决策可执行性 | 16 | relevant / supplementary | 买卖/持有/加仓/减仓/配置/仓位 |
| `risk_boundary_control` 风险控制与边界 | 12 | **始终 relevant** | 风险边界、匹配 |
| `product_universe_fit` 产品池与配置角色适配 | 按需 5-10 | relevant / supplementary | ETF/基金/资产组合/股票池 |
| `recommendation_stability` 推荐稳定性 | 按需 4-8 | relevant / supplementary | 历史对话、多次同类推荐 |
| `composition_credibility` 表达可信度 | 5 | **始终 supplementary** | |
| `tool_usage` 工具使用合理性 | 7 | **始终 relevant**（链路诊断） | |

**按需维度**：`product_universe_fit` 和 `recommendation_stability` 是从图片批注固化的按需维度，启用时从其他维度让出权重。

**可新增运行时维度**：

- `comparison_quantification` 多资产对比
- `private_advisor_continuity` 私人投顾连续性

---

## 六、7 个封顶规则（cap rules）

| 规则 | 上限 | 触发场景 |
|---|---:|---|
| `missing_kyc_profile` 缺失 KYC 画像 | **60** | 强 KYC 场景未主动取用 KYC 数据 |
| `misread_emotional_loss_context` 误读亏损/迷茫场景 | **50** | 浮亏题给短线抓反弹 |
| `fabricated_user_profile` 编造用户画像 | **55** | 模型编造 KYC 字段 |
| `missing_action_for_decision_request` 决策请求缺行动 | **65** | 问能不能买但不给可执行建议 |
| `missing_required_evidence` 必要证据缺失 | **60** | 推荐无证据支撑 |
| `overconfident_or_unsuitable_recommendation` 过度确定/不适当推荐 | **55** | 装确定 / 高波动推荐给保守型 |
| `template_generic_advice` 模板化通用建议 | **65** | 通用市场分析、热门标的清单、漂亮投顾模板 |

---

## 七、6 个 L1 根因归因体系

| L1 | 核心问题 |
|---|---|
| `intent` 理解问题 | 意图理解 |
| `context` **上下文/KYC 处理** | 是否读取/使用 KYC 数据 |
| `evidence` 检索证据 | 证据质量 |
| `tool` 选择与执行工具 | 工具使用 |
| `reasoning` 计算与推理 | 决策推理 |
| `composition` 组织答案 | 表达可信度 |
| `safety_or_compliance` **安全/合规边界** | 适当性、合规 |

`context` 和 `safety_or_compliance` 是本 skill 独有的 L1 阶段——**专门标记 KYC 数据使用缺失和安全/合规问题**。

---

## 八、关键评分原则（保守评分 6 条）

1. **最终答案决定用户侧质量**，链路只用于归因
2. **不要把"给了很多标的/指标/工具调用"自动视为高质量**
3. **KYC 推荐建议优先评估是否先理解人和场景**，再决定推荐、仓位、期限、风险边界
4. **"私人投顾感"是 05 类的重要质量标准** —— 答案要让用户看出模型知道我是谁、我处在什么投资状态
5. **对 05 类问题，高质量答案应主动使用用户 KYC 数据**。若链路没有取到 KYC，答案应说明画像依据不足，并给出分层、条件化、低风险边界清晰的建议或必要追问
6. **严惩编造用户画像、忽略亏损/迷茫/套牢情绪、把高风险短线策略推荐给明显不适配的用户**

---

## 九、强 KYC 标准细则

当前 v1 对 05 类问题采用**强 KYC 标准**：

- 只要问题属于投资推荐/配置建议/交易决策支持，就应检查模型是否主动获取并使用 KYC 数据
- KYC 数据来源：
  - 用户画像工具
  - 用户画像存储
  - 历史 `context`
  - 当前问题中的自述信息
  - 链路中可见的画像检索结果
- **不要把"context 中没有 KYC"作为放过模型的理由**
- 关键是模型面对这类问题时是否遵循"**先取 KYC、再做推荐**"的标准
- 若链路确实没有拿到可用 KYC，高质量答案应说明画像依据不足 + 分层/条件化/低风险边界 + 必要追问

---

## 十、13 个专家案例 + image_annotation_anchors

- 13 个专家案例 hard checks
- docx 截图红绿批注沉淀的**私人投顾感、产品池、稳定性、情绪场景和可执行动作** hard checks

---

## 十一、JSON 输出契约

**schema_version** = `kyc-recommendation-suggestions/v1`

工具列表直接复用 01（事件概念选股）的工具定义。

---

## 十二、与其他 skill 的边界

- ❌ **不适用**：纯行情查询、纯事实查询、客服问题、图片搜索、不需要用户适配的普通资料总结
- 与 **04-分析评价类问题**：以"是否需要给用户做适配后的决策建议"为准；04 仍需覆盖分析评价中夹带的"适合我/我的持仓/我的风险目标"类质量缺口
- 与 **06-复合意图**：本 skill 是 KYC 强约束；06 强调多子任务拆解
- 与 **13-时间感知**：本 skill 偏画像适配；13 偏时间锚点

---

## 快速上手 Checklist

1. **步骤 0** 必读 `rubric/_index.md`（10 维度 + 7 封顶）和 `golden_cases/_index.md`
2. **步骤 1** **对照 `meta.user_investment_goal` 评估画像适配**（suitability_personalization 18 分）
3. **步骤 2** **专门检查链路 KYC 读取动作** —— 缺失应在根因 summary 中明确写出"应使用用户 KYC 数据但未使用"
4. **步骤 3** 检查 7 个封顶（**特别注意 `missing_kyc_profile`**）
5. **步骤 4** 输出 JSON

**核心方法论**：「**先理解人 → 再看推荐 → 私人投顾感是关键**；强 KYC 标准不可让步。」
