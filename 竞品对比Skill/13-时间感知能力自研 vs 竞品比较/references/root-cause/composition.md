# composition

逻辑或证据可能存在，但最终答案是否把关键日期、市场状态、as-of 和替代口径清楚呈现给用户。

| L2 | 适用失败 | 常见维度 |
|---|---|---|
| asof-not-visible | 链路可能知道数据日期，但最终答案没有写清 | data_asof_freshness |
| correction-buried | 纠错信息被放在后文或弱化，用户仍会误解 | premise_correction_clarification |
| misleading-current-tense | 用“今天/当前/最新”等措辞包装旧数据 | answer_composition_credibility |

## 比较使用

如果一方链路查对但最终没说清，另一方链路较短但开头纠错且标注 as-of，比较结论应以最终用户可见质量为准。
