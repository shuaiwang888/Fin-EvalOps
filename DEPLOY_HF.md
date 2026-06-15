# Deploy Fin-EvalOps to Hugging Face Spaces

> 在 HF Space (Docker SDK) 上运行后端,用 **HF Datasets** 做 SQLite 持久化。
> 预计首次部署 10-15 分钟,后续 push 自动重部署。

## 1. 一次性准备(约 5 分钟)

### 1.1 创建 HF Dataset 仓库(持久化目标)

1. 打开 https://huggingface.co/new-dataset
2. 命名:建议 `fin-evalops-db`(可改,但要在 Space 环境变量同步)
3. Visibility:**Private**(默认)。里面的 `fin_evalops.db` 包含评测历史,可能有内部数据
4. 创建后记录:`owner` 字段(你的 username 或 org,下称 `<NAMESPACE>`)

> 首次推送时如果该 repo 不存在,`huggingface_hub` 也会自动创建,所以这步其实可以省略。
> 但**预先建好**可以省掉第一次拉取时的 404,且能立即验证 token 权限。

### 1.2 创建 Write Token

1. 打开 https://huggingface.co/settings/tokens
2. New token → **Write** 权限
3. 复制 token(下称 `<HF_TOKEN>`),存到密码管理器

### 1.3 创建 Space 仓库

1. 打开 https://huggingface.co/new-space
2. 命名:例如 `fin-evalops-backend`
3. Space SDK:**Docker**
4. Space hardware:**CPU basic**(免费)即可
5. Visibility:建议 **Private**
6. 创建后记录 Space URL(下称 `<SPACE_URL>`,形如 `https://huggingface.co/spaces/<NAMESPACE>/fin-evalops-backend`)

### 1.4 推送代码到 Space

Space 仓库与 GitHub 仓库**独立**。最简单的方式:

```bash
# 克隆 Space 仓库
git clone https://huggingface.co/spaces/<NAMESPACE>/fin-evalops-backend
cd fin-evalops-backend

# 把本仓库的内容拷进来(只拷运行时需要的)
# 注意:不要拷 backend/data/(含本地 db),不要拷 frontend/(独立部署)
rsync -av --exclude='.git' --exclude='frontend' --exclude='.pytest_cache' \
          --exclude='__pycache__' --exclude='backend/data' --exclude='.github' \
          /Users/appstore/AI-Code/Fin-EvalOps/ ./

# 推上去
git add .
git commit -m "Initial Fin-EvalOps backend"
git push
```

> 也可以用 HF 的 GitHub 集成(Space → Settings → Repository → connect to GitHub),这样 `git push` 到 GitHub 会自动同步到 Space。

## 2. 配置 Space Secrets

进入 Space → **Settings** → **Variables and secrets**,添加:

| 名称 | 类型 | 值 | 必填 |
|---|---|---|---|
| `HF_TOKEN` | **Secret** | `<HF_TOKEN>` | ✅ |
| `HF_NAMESPACE` | Variable | `<NAMESPACE>` | ✅ |
| `HF_DATASET_REPO` | Variable | `fin-evalops-db` | ❌(默认) |
| `HF_PUSH_INTERVAL` | Variable | `300` | ❌(默认 300 秒) |
| `ANTHROPIC_API_KEY` | **Secret** | `sk-ant-...` | 用于评测 |
| `OPENAI_API_KEY` | **Secret** | `sk-...` | 用于评测 |
| `DASHSCOPE_API_KEY` | **Secret** | `sk-...` | 用于评测 |
| `DEEPSEEK_API_KEY` | **Secret** | `sk-...` | 用于评测 |
| `MINIMAX_API_KEY` | **Secret** | `eyJ...` | 用于评测 |
| `MINIMAX_BASE_URL` | Variable | `https://api.minimaxi.com/anthropic` | ❌ |
| `DEFAULT_JUDGE_MODEL` | Variable | `claude-sonnet-4-6` | ❌ |
| `CORS_ORIGINS` | Variable | `https://shuaiwang888.github.io` | 前端用 |
| `IWENCAI_BASE_URL` | **Secret** | `https://117.50.195.94:2879` | 内网用 |
| `IWENCAI_VERIFY_SSL` | Variable | `false` | 内网自签证书 |

> Secret 不会出现在 logs 中。**绝对不要**用 Variable 存 key。

## 3. 触发构建 & 验证

Space 收到 push 后会自动构建,Logs 页可看到进度:

```
Building Docker image...
Step 1/12 : FROM python:3.11-slim
...
Step 8/12 : COPY backend/ /app/backend/
...
Successfully built abc123
Starting container...
✅ Pulled DB from HF: /data/fin_evalops.db (12.4 KB)     <-- 首次会跳过(没数据)
Synced 41 skills into DB
Started HF pusher (interval=300s)
Uvicorn running on http://0.0.0.0:7860
```

### 冒烟测试

```bash
SPACE="https://<NAMESPACE>-fin-evalops-backend.hf.space"

# 1) 健康检查
curl -fsS "$SPACE/api/health" | jq

# 2) 持久化状态(应该看到 hf_configured: true, dirty: false)
curl -fsS "$SPACE/api/admin/persistence" | jq

# 3) Skill 列表
curl -fsS "$SPACE/api/skills" | jq '.[0:3]'

# 4) 测试样本数量(应该 65)
curl -fsS "$SPACE/api/testsets/testcases?limit=200" | jq '.total'
```

第一次进 Space 时数据是空的(`/data` 是新挂载的临时盘 + Dataset 也没数据),这是正常。
所有读写 API 都可以直接用,只是跑评测产生的 Runs / Annotations 会**只存在到下次重启**,
需要触发一次 `POST /api/admin/persistence/push` 才会被推到 Dataset。

## 4. 持久化运维速查

```bash
SPACE="https://<NAMESPACE>-fin-evalops-backend.hf.space"

# 看当前是否 dirty
curl -fsS "$SPACE/api/admin/persistence" | jq '.dirty'

# 强制立即推送(忽略 dirty 标记)
curl -X POST "$SPACE/api/admin/persistence/push" | jq

# ⚠️ 危险:强制从 HF 拉取,会覆盖本地 DB(适合灾难恢复)
curl -X POST "$SPACE/api/admin/persistence/pull" | jq
```

后台推送线程默认 5 分钟一次。要更短/更长:

```
HF_PUSH_INTERVAL=60    # 1 分钟
HF_PUSH_INTERVAL=1800  # 30 分钟
HF_PUSH_INTERVAL=0     # 禁用(只剩批次结束 + shutdown 触发)
```

## 5. Sleep / Wake 与数据安全

HF Spaces **48 小时无访问后会自动 sleep**(免费层),wake 时容器**完全重启**——意味着:

1. 容器内 `/data/fin_evalops.db` **丢**
2. `lifespan` 启动 → `persistence.pull_db()` → 从 Dataset 拉回 ✓
3. 拉取时如果本地有非空 DB,会**跳过**(保护开发数据)
4. 首次 wake 后,DB 状态是上次最后一次 push 时的快照

**最坏数据丢失窗口** = `HF_PUSH_INTERVAL`(默认 5 分钟) + sleep 时的在途写入。
要更小:把 `HF_PUSH_INTERVAL` 调到 30~60 秒(频繁写 Dataset commit 会消耗 LFS 配额)。

## 6. 故障排查

### 6.1 构建失败:`ERROR: failed to solve`

最常见原因:`requirements.txt` 里某个包版本在 `python:3.11-slim` 上没 wheel。
解决:换 `python:3.11-bookworm` 或加 `--prefer-binary`。

### 6.2 启动后 502 / 反复重启

打开 Space → Logs,看崩溃栈。常见:
- `IWENCAI_BASE_URL` 配错 / 内网 IP 不可达 → evaluator 卡住 → HF pusher 也会卡
- `HF_TOKEN` 权限不足 → log 会出现 `403 Forbidden`
- `MINIMAX_BASE_URL` 路径写错 → LLM 调用全失败

### 6.3 DB 推不上去

```
HF push failed (reason=batch-end ...): 401 Client Error: Unauthorized
```
→ `HF_TOKEN` 过期或被 revoke,去 https://huggingface.co/settings/tokens 重新生成。

```
HF push failed: 409 Client Error: Conflict
```
→ Dataset repo 有并发 commit,重试即可(`huggingface_hub` 不会自动合并)。

```
HF push failed: Repository Not Found
```
→ 拼写错;或 token 对应的 user 没有该 namespace 的写权限。

### 6.4 前端连不上后端

CORS。在 `CORS_ORIGINS` 里加上前端地址,逗号分隔:

```
CORS_ORIGINS=https://shuaiwang888.github.io,http://localhost:5173
```

## 7. 升级 / 回滚

### 升级代码

```bash
cd /path/to/Fin-EvalOps
# 改代码...
git add . && git commit -m "feat: xxx"
# 推 GitHub
git push origin main
# 推 Space(如果用了 GitHub 集成就跳过这步)
cd ../fin-evalops-backend
git pull origin main
git push
```

Space 会自动 rebuild + redeploy。整个过程 ~2-5 分钟。

### 回滚到旧版

Space → **Settings** → **Factory rebuild**,或者 push 旧 commit:
```bash
cd fin-evalops-backend
git revert HEAD
git push
```

DB 不会回滚(它在 Dataset repo 里,跟代码独立)。

### 如果从旧平台迁过来(比如之前用过其他云)

迁完检查清单:

1. 在旧平台 Suspend / Delete 服务,避免空跑烧钱
2. 把之前填在旧平台的环境变量手动迁移到 HF Space Secrets(注意 `ANTHROPIC_API_KEY` 等是 Sensitive,**不要直接复制粘贴到聊天工具**,从密码管理器走)
3. 在前端 `VITE_API_BASE` Variable 改成新的 HF Space URL,然后**手动重跑一次 workflow**(push 不会自动重跑,Variable 改动要走 workflow_dispatch)
4. 用 `curl -fsS "$SPACE/api/health"` 验通,再用浏览器开前端试

## 8. 本地验证脚本

```bash
# 不需要启动 Space,直接测持久化模块
cd backend
python -c "
import os
os.environ['HF_TOKEN'] = 'hf_xxx'
os.environ['HF_NAMESPACE'] = 'yourname'
from app import persistence
print('configured:', persistence._hf_configured())
print('status:', persistence.is_dirty())
persistence.pull_db(force=True)  # 拉
persistence.push_db(reason='local-test', force=True)  # 推
"
```

更友好的脚本在 `backend/scripts/test_persistence.py`。
