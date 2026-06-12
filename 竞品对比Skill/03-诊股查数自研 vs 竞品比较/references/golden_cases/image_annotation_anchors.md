# 图片与截图补充锚点

本文件沉淀 docx 截图和图表中可用于自动评测的补充知识。由于截图通常承载好坏答案对照，评分时用于加强呈现、图表、工具失败归因和专家风格判断。

## 图表与可视化

- 分红总额、年度涨跌幅、多年指标序列、行业板块跑赢指数等场景，图表和表格是明确加分项。
- 图表不能替代计算和解释。若答案有图但没有年度差距、累计总额、强弱排序或结论，仍需扣 `calculation_comparison` 和 `insight_extension`。
- 对比图应保证同口径、同时间区间、单位清楚；图表口径不明会影响 `time_caliber_precision` 和 `presentation_visualization`。
- 数据密集题应先给结论，再给表格/图表，再给口径和观察点。

## 好答案截图特征

- 对模糊问题会先锚定最新事件或最可能时间，例如"什么时候分红"同时回答最近一次和今年进展。
- 对诊断问题会按市场框架拆解，而不是只抛字段。
- 对取数问题会给多周期连续性和多维扩展：当前值、历史趋势、同比/环比、相关指标。
- 对非结构化信息会尝试搜索、公告、研报、调研纪要，并说明证据边界。
- 对行业/板块跑赢问题会补充标志性成分股表现和驱动分析。

## 坏答案截图特征

- 只用结构化库一个冷门字段回答复杂市场问题，例如用"集中度90"回答筹码集中度。
- 对"主力"只看资金流，不看龙虎榜或知名席位。
- 对"增长点"罗列公司存量业务优势，没有客户突破、订单、市占率或边际变化。
- 对"止盈位"只给单一价格，缺少技术位、成本、周期、仓位和风险收益逻辑。
- 对跨市场商品比价只用经验汇率或经验比例，未查询汇率和合约口径。
- 工具查不到就停，没有尝试补充来源，也没有说明局限。

## 工具失败归因图锚点

专家文档总结的金融查询工具问题中，模型 SQL 问题占工具错误的最大比例；另有取数问题、linking 问题、指标配置问题、指标覆盖问题、取数 SQL 问题、数据效果问题和长问句拆解问题。用于归因时可按以下方式映射：

- SQL/条件解析错误：归因 `tool/sql-condition-parse-error`，常影响 `data_accuracy_coverage`、`time_caliber_precision`。
- 取数上限或接口缺失：归因 `tool/tool-limit-not-handled` 或 `evidence/data-completeness-gap`。
- linking 错误：归因 `tool/tool-input-error` 或 `evidence/wrong-data-value`。
- 指标配置/覆盖问题：归因 `evidence/data-completeness-gap` 或 `tool/wrong-tool-selection`。
- 长问句拆解失败：归因 `intent/subtask-missed` 或 `reasoning/comparison-not-synthesized`。

## 人工复核更新规则

当专家采样 review 给出新的失败样本时：
- 如果是具体 query 类型，优先补充到 `golden_cases/_index.md`，写成 hard checks。
- 如果是跨样本稳定规律，补充到对应 rubric 维度或封顶规则。
- 如果是链路阶段问题，补充到 root-cause 的 L2；不要把根因写进评分维度里。
- 如果是工具能力或数据源缺口，补充到 tool_usage、tool root cause 或工具列表说明。
