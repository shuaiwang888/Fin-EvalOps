# L1：理解问题

用于解释模型没有识别用户真实咨询目标。

L2：
- `surface_intent_only`：只按字面问题回答，没有识别真实交易/咨询目标。
- `hidden_need_missed`：遗漏用户隐含的风险、权限、标的、回本或行动需求。
- `sub_question_omitted`：多目标咨询中遗漏关键子问题。
- `risk_intent_missed`：用户实际在询问风险或能否操作，但答案只给机会或知识。

证据常来自 `question`、`text_answer` 和 `context`。
