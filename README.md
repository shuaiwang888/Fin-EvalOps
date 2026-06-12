# Fin-EvalOps

> 金融 Agent 评测运维平台 · 13 类自研评测 Skill × 65 真实金融问句样本 × 多模型 LLM Judge

针对金融 Agent 输出做**自动化评测**:输入金融问句,Agent 自动路由到对应的 13 类自研评测 Skill 之一,按"5 步评测协议 + 六档分量表 + 封顶规则 + 根因归因"产出结构化结果,Web 端可视化展示分数趋势、雷达图、根因时间线,并支持 Data Agent 对话式分析。

## 仓库分区

```
Fin-EvalOps/
├── 自研评测Skill/         # 13 个自研评测协议(read-only)
├── 竞品对比Skill/         # 14 个竞品对比协议(read-only, 二期接入)
├── 端到端Skill/           # 14 个端到端协议(read-only, 二期接入)
├── 数据测试集/            # 65 条真实金融测试样本(13 分类 × 5 条)
├── fetch_eval_record.py  # 从问财 EvalOps 后端拉取评测明细(后端 import 复用)
├── backend/              # FastAPI + SQLAlchemy + SQLite
└── frontend/             # Vite + React + TS + AntD + ECharts
```

## 本地启动

### Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # 填入 LLM API key(本地开发)
uvicorn app.main:app --reload --port 8000
```

打开 `http://localhost:8000/docs` 查看 OpenAPI。

### Frontend (Node 20+)
```bash
cd frontend
npm install
cp .env.example .env       # VITE_API_BASE=http://localhost:8000
npm run dev
```

打开 `http://localhost:5173`。

## 部署

仓库:[github.com/shuaiwang888/Fin-EvalOps](https://github.com/shuaiwang888/Fin-EvalOps)

| 端 | 平台 | 入口 |
|---|---|---|
| Backend | [Render](https://render.com) Web Service | `backend/render.yaml` Blueprint |
| Frontend | GitHub Pages: `https://shuaiwang888.github.io/Fin-EvalOps/` | `.github/workflows/deploy.yml` |

### 敏感信息约束(强制)

- LLM API key 仅存放在 Render Dashboard 环境变量中,前端代码与 GitHub Pages 仓库**绝不包含**任何 key
- 问财 EvalOps 内网地址 `IWENCAI_BASE_URL` 仅后端可见,前端只暴露受控的 `/api/testsets/import-from-iwencai`
- 部署前自检:`grep -rE '117\.50\.195\.94|sk-[a-zA-Z0-9]{20,}' frontend/dist/` 必须为空

## 文档

- 整体方案:`/Users/appstore/.claude/plans/skill-skill-adaptive-cat.md`
- 自研评测协议总览:[`自研评测Skill/README.md`](自研评测Skill/README.md)
