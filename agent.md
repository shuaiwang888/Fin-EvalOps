# Agent Notes — Fin-EvalOps

Notes left by coding agents for future agents. Read this before making changes.

---

## Architecture in 30 seconds

- **Backend**: FastAPI + SQLAlchemy + SQLite (WAL). Lives in `backend/app/`. Routers: `testsets`, `runs`, `skills`, `dashboard`, `agent`, `annotations`, `sse`. Background eval work in `services/evaluator.py`.
- **Frontend**: Vite + React + TS + AntD + ECharts. Lives in `frontend/src/`. Key page: `pages/TestSets/index.tsx`.
- **Eval pipeline**: `TestCase` → auto-route to a `Skill` (`services/skill_router.py`) → LLM judge (`services/llm_client.py`) → store on `Run` with `weight_assignment`, `dimension_scores`, `caps`, `root_causes`, `narrative_review`.
- **Deployment**:
  - Frontend → GitHub Pages (auto via `.github/workflows/deploy.yml` on push to `main` touching `frontend/**`).
  - Backend → HF Space `appqqq/Fin-EvalOps-v2` (Docker SDK). NOT auto-synced from GitHub unless the user manually enables GitHub integration in the Space settings.
- **Persistence**: SQLite DB lives in `/data` on the Space, snapshot-pushed to a HF Dataset repo via `persistence.py`.

---

## Recent work (2026-06 → 2026-07)

### Feature: custom business categories

Business asked: don't force every eval batch into one of the 13 seeded self-eval categories. Let users define their own.

- Backend ([`routers/testsets.py`](backend/app/routers/testsets.py)): new `POST /api/testsets/categories` (with body validation: code charset = `^[\w一-鿿\-]+$`, length 1-32) and `DELETE /api/testsets/categories/{code}` (refuses seed `is_custom=false` with 409; refuses in-use categories).
- Model ([`models.py`](backend/app/models.py)): `TestCategory.is_custom: Boolean` + inline migration. Widened `code` / `category_code` to `String(64)` — SQLite type affinity means no DDL migration needed.
- Slug auto-derived as `c-{slugified-code}` to keep custom in its own namespace and avoid colliding with the canonical English slugs.
- Frontend ([`pages/TestSets/index.tsx`](frontend/src/pages/TestSets/index.tsx)): `+ 新建分类` button next to the category Select in all 3 modals (import / new / iwencai-pull); new top-toolbar `分类管理` modal with delete popconfirm; tree node title appends 🏷️ for custom rows.

### Fix: `tags` lost across all JSON import paths

`_normalize_raw` (Chinese-keyed branch) didn't extract `tags`; `import_file` / `scan_disk` / `import-from-iwencai` never wrote `tags=...` to the `TestCase` ORM. Result: any upstream metadata packed into `tags` (e.g. by `scripts/convert_part06.py`) silently disappeared. Fixed in the same PR — `tags=norm.get("tags")` now propagates everywhere.

### Fix: scan-disk `500` when `testsets_root` is missing

`数据测试集/` is now uploaded at runtime via the web UI instead of bundled in the Docker image (see "Things you must know" below). Without data on disk, `POST /api/testsets/scan-disk` returned 500. Fixed: now returns `ScanDiskResponse(scanned=0, inserted=0, updated=0, skipped=0)` and the frontend's "磁盘同步" button just shows 0 instead of erroring.

### Fix: eval pipeline — parallel-array `root_causes` + tool_use text-block recovery

Two recurring eval failures observed in user runs:

1. **Judge outputs `root_causes` as a dict of parallel arrays** (e.g. `{l1: ["a","b"], l2: ["x","y"], raw_score: ["40","60"], …}`) when the schema wants a list of objects. Same pattern occasionally on `caps`, `skipped_dimensions`. Validator throws `SchemaValidationError`.
2. **minimax / other Anthropic-compatible APIs** put JSON in a markdown text block instead of a `tool_use` block. The fallback tried to validate strictly; on failure the entire eval died.

Fix in [`services/llm_client.py`](backend/app/services/llm_client.py):

- New `_sanitize_judge_for_validation()` runs **before** strict validation. Detects "dict of parallel arrays" shape and transposes to list of objects. Coerces `raw_score` / `score_ceiling` string-numbers to float. Splits string `matched_golden_cases` into list.
- `call_with_schema` now wraps validation: if it fails, fills missing `required` fields with empty defaults, re-validates; if still failing, returns partial data with a warning instead of raising. Downstream evaluator sanitizers can recover the rest.
- `_call_anthropic` text-block fallback: pre-sanitizes, then on residual mismatch logs a warning and returns data anyway.

Duplicate sanitizer in [`services/evaluator.py`](backend/app/services/evaluator.py) `_sanitize_judge_output` — defense in depth, handles cached / out-of-band payloads.

### Frontend: explicit "开始导入" button on the JSON import modal

The Antd `Upload.beforeUpload` was firing the import the moment a file was selected, and `Modal.footer={null}` hid the default OK/Cancel. Users had no way to confirm the action. Now: file is staged in state; `开始导入` OK button (disabled until both category + file are set) triggers `importFile`; success message includes the destination category code.

---

## Things you must know (operational gotchas)

### HF Space sync — there is NO direct git push from this environment

`git push` to `huggingface.co/spaces/...` fails from this machine (network policy blocks port 443 to `huggingface.co`). The workaround is `huggingface_hub.HfApi`:

```python
from huggingface_hub import HfApi
api = HfApi(token=open("/Users/appstore/.cache/huggingface/token").read().strip())
api.upload_file(
    path_or_fileobj=open("local/file", "rb").read(),
    path_in_repo="remote/path",
    repo_id="appqqq/Fin-EvalOps-v2",
    repo_type="space",
    commit_message="...",
)
```

`HfApi` uses an HTTP API path that *is* reachable; raw `git` over SSH or HTTPS to `huggingface.co` is not. Endpoints like `model_info("gpt2")` work without auth; authenticated writes need the cached token at `~/.cache/huggingface/token`.

`upload_folder` is for many files at once (uses LFS for large ones); `upload_file` is for a single file commit. `delete_files(repo_id, repo_type, delete_patterns=[...])` removes files with glob patterns.

SSL is intermittent — wrap writes in a retry loop. Each `upload_file` / `delete_files` creates its own commit, so failures mid-upload don't roll back earlier commits.

If a fresh user runs into the same `git push` failure, use the script at `scripts/sync_to_hf_space.sh` which clones locally + rsyncs + commits (assumes the user can reach huggingface.co from their machine).

### Dockerfile: do NOT `COPY 数据测试集/`

The Docker image must not bundle test data. The pattern is:

```dockerfile
COPY backend/ /app/backend/
COPY skills/  /app/skills/
# 数据测试集/ is NOT bundled — tests are uploaded via the web UI.
```

If you add the COPY line back, the build fails with `"/数据测试集/自研评测测试集": not found` (because the directory is excluded from the Space repo via the deletion commit `7d79f77a1f13`).

### `.hfignore` keeps test data out of HF uploads

`/Users/appstore/AI-Code/Fin-EvalOps/.hfignore` excludes `数据测试集/`, `*.jsonl`, and `_smoke_*.json`. Also `scripts/sync_to_hf_space.sh` has matching rsync excludes. Don't re-add these — they were excluded for a reason (don't bundle customer test data into the Space image).

### SQLite migration pattern is `_run_inline_migrations()`

Adding a column? Put it in the `MIGRATIONS` list in [`backend/app/db.py`](backend/app/db.py) with a predicate + action SQL. Predicate should return 1+ rows when migration is needed. SQLite ALTER TABLE only supports ADD COLUMN and RENAME COLUMN — for anything more complex (e.g. widening column type), you need table rebuild or just leave the schema declaration alone (SQLite doesn't enforce VARCHAR length anyway).

### `TestCase` is referenced everywhere — be careful with column changes

`TestCase` is the central model. Test cases are created from JSON import, manual API, scan-disk, iwencai import. If you change a column, update:
- The model in `models.py`
- `_normalize_raw` (handles Chinese-keyed JSON)
- All 4 creation paths: `import_file`, `scan_disk`, `import-from-iwencai`, `create_testcase`
- The serializer (`schemas.py`)

Missing any path → silent data loss (this is exactly what bit us with `tags`).

---

## Testing

```bash
cd backend && python3 -m pytest tests/ -v
```

49 tests, all passing. Patterns:
- `test_field_rename.py` — DB-level migration tests (create temp DB with old schema, run migration, verify shape).
- `test_custom_category.py` — full-stack via `TestClient` with patched DB session.
- `test_sanitize_judge_output.py` — pure-function tests for LLM output reshaping (the 12 new cases cover parallel-array transpose + permissive fallback).
- `test_skill_router.py`, `test_scorer.py`, `test_cache_headers.py`, `test_sanitize_judge_output.py` (legacy) — unit tests.

For end-to-end smoke tests against a live Space, you'll need an LLM API key. The HF Space has provider keys configured; for local testing set `MINIMAX_API_KEY` (or others) in env and run `uvicorn app.main:app --port 8000`.

---

## File map (for agents coming in cold)

```
Fin-EvalOps/
├── backend/app/
│   ├── main.py                   # FastAPI app, lifespan (HF persistence + skill sync)
│   ├── config.py                 # Settings, env-driven
│   ├── db.py                     # SQLite engine, migrations
│   ├── models.py                 # ORM models (TestCase, Run, Skill, TestCategory, ...)
│   ├── schemas.py                # Pydantic I/O schemas
│   ├── persistence.py            # HF Datasets snapshot push/pull
│   ├── routers/
│   │   ├── testsets.py           # ← most custom-category work lives here
│   │   ├── runs.py               # Run creation + polling
│   │   ├── skills.py             # Skill catalog API
│   │   ├── dashboard.py
│   │   ├── agent.py              # Data Agent (LLM chat over the DB)
│   │   ├── annotations.py
│   │   └── sse.py                # SSE channels for live progress
│   └── services/
│       ├── llm_client.py         # ← sanitizer fixes live here
│       ├── evaluator.py          # ← 5-step eval pipeline; _sanitize_judge_output here
│       ├── scorer.py             # weighted-sum + cap rule application
│       ├── skill_router.py       # auto-route question → skill
│       ├── skill_loader.py       # parses 自研评测Skill/ markdown into Skill rows
│       ├── data_agent.py         # Data Agent LLM prompt
│       └── fetch_iwencai.py      # iwencai EvalOps backend adapter
├── frontend/src/
│   ├── pages/TestSets/           # ← UX overhaul for custom categories lives here
│   ├── api/testsets.ts           # frontend API client (createCategory, deleteCategory)
│   └── components/, pages/{Agent,Annotations,Compare,Dashboard,Runs,Skills,Settings}/
├── skills/                       # 13 self-eval + 14 competitor + 14 e2e skill markdown
├── scripts/
│   ├── convert_part06.py         # JSONL → platform-importable JSON converter
│   └── sync_to_hf_space.sh       # git-based HF Space sync (only works for users with network access)
├── 数据测试集/                   # ⚠️ NOT shipped to Space (excluded in .hfignore)
│   ├── 自研评测测试集/             # 13 canonical test set files
│   ├── 竞品对比测试集/
│   ├── part_06.jsonl             # new test data (user's)
│   └── part_06-importable.json   # generated by scripts/convert_part06.py
├── .hfignore                     # excludes data from HF uploads
└── Dockerfile
```

---

## Common tasks

### Add a new eval metric dimension

1. Update the skill's markdown in `skills/自研评测Skill/<NN>-<slug>/` (add dim to dimensions table, caps table, root_causes table).
2. Update the LLM schema in [`backend/app/services/evaluator.py`](backend/app/services/evaluator.py) `EVAL_OUTPUT_SCHEMA` `dimension_scores.additionalProperties` if you want strict validation.
3. The schema is shared across all 13 skills — don't break the others. If a dimension is skill-specific, define it per-skill via a relaxed schema.

### Add a new business category via API

```bash
curl -X POST https://appqqq-fin-evalops-v2.hf.space/api/testsets/categories \
  -H 'Content-Type: application/json' \
  -d '{"code":"my-batch-2026q3","name_zh":"2026Q3 回归批次","description":"..."}'
```

Returns `TestCategoryOut` with `is_custom: true`, `slug: c-my-batch-2026q3`.

### Import a test set into a custom category

```bash
curl -X POST 'https://appqqq-fin-evalops-v2.hf.space/api/testsets/import-file?category_code=my-batch-2026q3' \
  -F 'file=@my_set.json'
```

Response: `{"inserted": N, "total_in_file": M}`. Returns 400 if the category doesn't exist; the import endpoint accepts both Chinese-keyed (`{问题, 答案, 链路数据, 上下文, id, 来源, tags}`) and English-keyed (`{question, agent_answer, reasoning_trace, context_history, source_id, source, tags}`) JSON.

### Trigger a single eval

```bash
curl -X POST https://appqqq-fin-evalops-v2.hf.space/api/runs \
  -H 'Content-Type: application/json' \
  -d '{"testcase_id":"<hex>","judge_model":"minimax-3"}'
```

Returns 201 with the run. Poll `GET /api/runs/{run_id}` for status. Auto-routes to the best matching skill unless `skill_id` is provided.

---

## Known rough edges (not bugs, just be aware)

- `cost_usd` is always `null` — `ModelSpec` has no pricing fields. If you add pricing, update `LLMResult` and the evaluator to compute `tokens_in * input_price + tokens_out * output_price`.
- `matched_golden_cases` is often `[]` even when the question clearly matches a golden case — judge models tend to be conservative. The golden case list is provided in the prompt (truncated to 6000 chars).
- `scan-disk` always returns 0 on the Space (no bundled data). This is intentional after the 2026-07 cleanup.
- HF Space file count is ~1598 because the previous sync included `.pytest_cache/` etc. These are harmless dead files but inflate the repo. Safe to ignore.