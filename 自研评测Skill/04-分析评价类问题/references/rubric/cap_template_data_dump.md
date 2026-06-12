# 封顶规则：`template_data_dump`

分数上限：`60`

当答案主要是模板化结构或数据堆砌，无法体现本题关键判断时触发。

触发条件：
- 对所有股票都套“技术面、基本面、资金面、消息面”，没有个股核心逻辑
- 长表格或指标罗列替代投资论点
- 资讯拼接很多，但没有形成判断、传导链或决策含义
- 答案篇幅很长但信息密度低，关键结论、证据和行动建议被淹没

不触发条件：
- 数据表服务于清晰论点，并且有必要解读。

根因优先映射：
- `composition.data-dumping`
- `composition.generic-template-answer`
- `reasoning.no-investment-thesis`
