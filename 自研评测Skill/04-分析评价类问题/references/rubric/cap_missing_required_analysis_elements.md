# 封顶规则：`missing_required_analysis_elements`

分数上限：`65`

当某类问题有专家明确要求的必备要素，但答案缺失关键项时触发。

触发条件示例：
- 基金诊断缺少历史收益、最大回撤、夏普、同类排名、前十大持仓风格中的多数关键项
- 估值历史位置问题未提供历史分位、区间或多市场口径
- 对比切换问题未逐项比较核心差异
- 宏观资产分析没有时间区间和配置含义

不触发条件：
- 缺少少量辅助指标，但主分析框架完整。

根因优先映射：
- `intent.required-elements-missed`
- `evidence.missing-critical-metrics`
- `composition.plan-answer-drop`
