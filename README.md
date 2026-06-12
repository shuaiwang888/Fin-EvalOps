# Fin-EvalOps

> 金融 Agent 评测运维平台 · 13 类自研评测 Skill × 65 真实金融问句样本 × 多模型 LLM Judge

针对金融 Agent 输出做**自动化评测**:输入金融问句,Agent 自动路由到对应的 13 类自研评测 Skill 之一,按"5 步评测协议 + 六档分量表 + 封顶规则 + 根因归因"产出结构化结果,Web 端可视化展示分数趋势、雷达图、根因时间线,并支持 Data Agent 对话式分析。

## 🟢 在线访问

| 端 | URL | 状态 |
|---|---|---|
| Backend  | https://fin-evalops-backend.onrender.com | 已部署 · `/api/health` 可访问 |
| Frontend | https://shuaiwang888.github.io/Fin-EvalOps/ | 待启用 GitHub Pages |
| Repo     | https://github.com/shuaiwang888/Fin-EvalOps | — |

## 仓库分区

```
Fin-EvalOps/
├── skills/                # 三类评测协议(read-only)
│   ├── 自研评测Skill/     #   13 个自研评测协议(P0 已接入)
│   ├── 竞品对比Skill/     #   14 个竞品对比协议(P2 接入)
│   └── 端到端Skill/       #   14 个端到端协议(P2 接入)
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
| Backend | [Render](https://render.com) Web Service | `render.yaml` Blueprint(仓库根目录) |
| Frontend | GitHub Pages: `https://shuaiwang888.github.io/Fin-EvalOps/` | `.github/workflows/deploy.yml` |

### Render 免费层的数据持久化

免费层**无持久磁盘**,SQLite 存在容器内的 `./data/`,重启或重新部署会丢。但:

- **Skill 元数据 (41 个)** 和 **测试样本 (65 条)** 在 lifespan 启动时自动从仓库重建,不需要手动操作
- **会丢的**只有用户产生的 `Runs` / `Annotations` / `AgentSessions` 历史

升级方式:
- 加付费 disk(`$1/月` 起,在 render.yaml 中重新添加 `disk:` 块)
- 切换到 Render PostgreSQL(免费 90 天后 `$7/月`),把 `DB_PATH` 改成 `postgresql://...`

### 敏感信息约束(强制)

- LLM API key 仅存放在 Render Dashboard 环境变量中,前端代码与 GitHub Pages 仓库**绝不包含**任何 key
- 问财 EvalOps 内网地址 `IWENCAI_BASE_URL` 仅后端可见,前端只暴露受控的 `/api/testsets/import-from-iwencai`
- 部署前自检:`grep -rE '117\.50\.195\.94|sk-[a-zA-Z0-9]{20,}' frontend/dist/` 必须为空

## 文档

- 整体方案:`/Users/appstore/.claude/plans/skill-skill-adaptive-cat.md`
- 自研评测协议总览:[`自研评测Skill/README.md`](自研评测Skill/README.md)
