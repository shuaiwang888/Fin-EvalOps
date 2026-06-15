# Fin-EvalOps Backend

FastAPI + SQLAlchemy + SQLite,负责 Skill 路由、5 步评测协议执行、Run 持久化与聚合。

## 快速开始

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 填入 LLM key
uvicorn app.main:app --reload --port 8000
```

## 启动后第一步:同步 Skill + 测试集

```bash
curl -X POST http://localhost:8000/api/skills/reload
curl -X POST http://localhost:8000/api/testsets/scan-disk
```

或访问 [http://localhost:8000/docs](http://localhost:8000/docs) 调用接口。

## 模块

| 模块 | 文件 | 说明 |
|---|---|---|
| 配置 | `app/config.py` | pydantic-settings 读取环境变量 |
| 数据库 | `app/db.py` `app/models.py` | SQLAlchemy 2.0 ORM |
| Skill 加载 | `app/services/skill_loader.py` | 扫描"自研评测Skill/"目录,解析 frontmatter + references/* |
| 路由 | `app/services/skill_router.py` | 关键词预筛 + LLM 判定 |
| 评测 | `app/services/evaluator.py` | 5 步协议执行 |
| 计分 | `app/services/scorer.py` | 加权 + 封顶 + 根因 |
| LLM | `app/services/llm_client.py` | Claude/GPT/通义/DeepSeek 多 provider |
| Data Agent | `app/services/data_agent.py` | 自然语言→SQL→图表 |

## 部署 (HF Space)

后端部署到 **Hugging Face Space (Docker SDK)**,持久化走 **HF Datasets**。详细操作见仓库根目录的 [DEPLOY_HF.md](../DEPLOY_HF.md)。
部署完成后只需在 Space → Settings → Variables and secrets 中设置 LLM key + `IWENCAI_BASE_URL` + `CORS_ORIGINS` 等敏感/可变参数。
