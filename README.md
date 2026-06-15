---
title: Fin-EvalOps
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: 13 类金融 Agent 评测 Skill × 多模型 Judge × Web 评测平台
---

# Fin-EvalOps

> 金融 Agent 评测运维平台 · 13 类自研评测 Skill × 65 真实金融问句样本 × 多模型 LLM Judge

针对金融 Agent 输出做**自动化评测**:输入金融问句,Agent 自动路由到对应的 10+ 类自研评测 Skill 之一,按"5 步评测协议 + 六档分量表 + 封顶规则 + 根因归因"产出结构化结果,Web 端可视化展示分数趋势、雷达图、根因时间线,并支持 Data Agent 对话式分析。

## 🟢 在线访问

| 端 | URL | 状态 |
|---|---|---|
| Backend  | `https://<your-space>.hf.space` (Docker SDK) | 主部署 · HF Space |
| Frontend | https://shuaiwang888.github.io/Fin-EvalOps/ | GitHub Pages |
| Repo     | https://github.com/shuaiwang888/Fin-EvalOps | — |

> 后端部署在 Hugging Face Spaces (Docker SDK),详见 [DEPLOY_HF.md](DEPLOY_HF.md)。

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
│   └── app/persistence.py  # HF Datasets 持久化层(新增)
├── frontend/             # Vite + React + TS + AntD + ECharts
├── Dockerfile            # HF Space 构建(新增)
├── DEPLOY_HF.md          # HF Space 部署指南(新增)
```

## 数据持久化方案(★ 新)

容器磁盘是**临时**的(Space 重启 / sleep-wake / 重新部署都会清空)。本项目用 **Hugging Face Datasets** 当持久层:

- **存储位置**:`<HF_NAMESPACE>/<HF_DATASET_REPO>` 仓库的 `fin_evalops.db` 文件
- **拉取**:每次 `lifespan` 启动,如果本地 DB 不存在或为空,自动从 Dataset 拉取
- **推送触发点**:
  - 每次 `evaluate_batch` 结束(自然业务单位)
  - 后台线程(默认 5 分钟,`HF_PUSH_INTERVAL` 可调)
  - 应用关闭(SIGTERM 时 `tini` 转发信号触发 `lifespan` 退出)
- **快照方式**:SQLite 在线 backup API(`Connection.backup()`),保证一致性
- **禁用方式**:不设置 `HF_TOKEN` 或 `HF_NAMESPACE` 即关闭全部持久化(纯本地模式)

详细 API 与运维命令见 [DEPLOY_HF.md](DEPLOY_HF.md)。

## 本地启动

### Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # 填入 LLM API key(本地开发)
# 可选:填 HF_TOKEN / HF_NAMESPACE 启用 Datasets 持久化
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

| 端 | 平台 | 入口 |
|---|---|---|
| Backend | **Hugging Face Space** (Docker SDK) | [DEPLOY_HF.md](DEPLOY_HF.md) |
| Frontend | GitHub Pages: `https://shuaiwang888.github.io/Fin-EvalOps/` | `.github/workflows/deploy.yml` |

### 敏感信息约束(强制)

- LLM API key 仅存放在 **HF Space Secrets** 中,前端代码与 GitHub Pages 仓库**绝不包含**任何 key
- 问财 EvalOps 内网地址 `IWENCAI_BASE_URL` 仅后端可见,前端只暴露受控的 `/api/testsets/import-from-iwencai`
- 部署前自检:`grep -rE '117\.50\.195\.94|sk-[a-zA-Z0-9]{20,}' frontend/dist/` 必须为空

## 文档

- 整体方案:`/Users/appstore/.claude/plans/skill-skill-adaptive-cat.md`
- 自研评测协议总览:[`自研评测Skill/README.md`](自研评测Skill/README.md)
- HF Space 部署:[DEPLOY_HF.md](DEPLOY_HF.md)
