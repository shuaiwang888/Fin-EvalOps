# 评分细则索引

## 维度列表

| 维度 | 建议权重 | 适用性判断 |
|---|---:|---|
| `semantic_intent_alignment` 语义意图匹配 | 20 | 始终 relevant。判断是否读懂用户真实对象、真实任务和隐含语义 |
| `financial_term_understanding` 金融术语/规则理解 | 20 | 涉及金融术语、交易规则、市场黑话、财务概念时 relevant |
| `entity_product_boundary` 实体与产品边界 | 15 | 涉及同名公司、股票/基金/ETF/指数/现货、旗下产品时 relevant |
| `metric_caliber_accuracy` 指标公式与数据口径 | 15 | 涉及 PE、ROE、主力控盘、ST、披露期、盘中价格等口径时 relevant |
| `timeliness_context` 时效上下文 | 10 | 涉及最新、近期、当下、盘中、报告期时 relevant；其他题目 supplementary |
| `credibility_expression` 可信解释与表达 | 10 | 始终 supplementary，若用户要求解释或定义则 relevant |
| `tool_usage` 工具使用合理性 | 10 | 始终 relevant |

## 动态权重

- 仅基于用户问题分配适用性和权重。
- `relevant` 维度获得主权重，`supplementary` 一般 3-10，`not_applicable` 为 0。
- 权重总和必须为 100。
- 若题目只考察定义/常识，`credibility_expression` 可提高到 15-20。
- 若题目涉及实体错配或产品边界，`entity_product_boundary` 至少 15。

## 关键扣分方向

- 把用户真实对象理解错：例如黄金实物问成 ETF、豪威集团答成豪能股份。
- 概念只会查数，不会解释：例如问微盘股定义却给流通市值数据。
- 规则硬错：例如集合竞价 9:20 当成已成交量、最新季度 ROE 使用未披露报告期。
- 指标口径失真：例如 PE 最小直接包含负 PE、主力控盘比例不解释定义。
- 新题材或黑话误判：例如 Token 只按区块链理解，老登股只按上市年限理解。
