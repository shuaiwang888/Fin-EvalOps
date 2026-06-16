# Fin-EvalOps Frontend

Vite + React + TS + AntD + ECharts。前端**永不**接触 LLM key 或问财后端 URL。

## 本地开发

```bash
cp .env.example .env       # 默认通过 Vite proxy 走 localhost:8000
npm install
npm run dev                # http://localhost:5173
```

## 部署 (GitHub Pages)

1. 在 GitHub 仓库 Settings → Pages 设置 Source 为 "GitHub Actions"
2. Settings → Secrets and variables → Actions → **Variables**(注意是 Variables 不是 Secrets)添加:
   - `VITE_API_BASE` = `https://<your-namespace>-fin-evalops.hf.space` (去掉尾部 `/`,例 `https://appqqq-fin-evalops-v2.hf.space`)
   - `VITE_BASE_PATH` = `/Fin-EvalOps/` (子路径) 或 `/` (apex domain)
3. push 到 main,Actions 自动构建并发布到 `gh-pages` 分支
4. 改完 Variable 必须**手动重跑一次 workflow**,否则会继续用上一次构建时烤进 bundle 的旧 URL

## 安全自检

构建前自动跑 `scripts/check-no-secrets.mjs`,扫到 LLM key/内网 IP 字面量则失败:

```bash
npm run check-no-secrets
```

CI 还会在 `dist/` 构建产物上再做一次 grep,双保险。

## 页面

| 路径 | 模块 |
|---|---|
| `/` | Dashboard — 13 Skill 雷达、L1 根因、30 天趋势、Top 失败 |
| `/testsets` | 测试集管理(CRUD + 文件导入 + 问财拉取 + 磁盘扫描) |
| `/skills` | Skill 三 Tab(自研/竞品/端到端) + 详情 + 源文件预览 |
| `/runs` | 评测任务列表 + 单条/批量创建 + 实时 SSE 进度 |
| `/runs/:id` | 单 Run 详情:路由、雷达、维度表、封顶、根因时间线、报告 |
| `/agent` | Data Agent 对话式数据分析(SQL + 图表) |
| `/compare` | (P1) Run A vs Run B 并排对比 |
| `/annotations` | (P1) 人工标注覆盖 LLM judge |
| `/settings` | (P2) Skill 编辑器 + 后端诊断 |
