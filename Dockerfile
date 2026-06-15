# =============================================================================
# Fin-EvalOps backend — Docker image for Hugging Face Spaces (Docker SDK)
#
# Build context: repository root.
# Runtime layout (matches config.py's parents[2] = project root):
#   /app/
#     backend/             # FastAPI app
#     skills/              # 13 self-eval + 14 competitor + 14 e2e skill protocols
#     数据测试集/           # 65 test samples across 13 categories
#   /.cache/huggingface/   # HF Hub cache (datasets, models)
#   /data/                 # SQLite DB (ephemeral — synced to HF Dataset)
# =============================================================================

FROM python:3.11-slim AS base

# System deps: curl for healthcheck, tini for clean signal handling, git for
# huggingface_hub's snapshot_download fallback.
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        tini \
        git \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces exposes the app on port 7860 (or the value of $PORT).
# Make the port explicit for clarity; uvicorn reads $PORT at runtime.
ENV PORT=7860 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Tell huggingface_hub where to put its cache (and where to look first
    # when downloading dataset files). Persistent across rebuilds in the
    # image layer; not persistent across Space restarts (intentional).
    HF_HOME=/.cache/huggingface \
    TRANSFORMERS_CACHE=/.cache/huggingface/hub

WORKDIR /app

# ---- Python deps (cache layer) ----
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# ---- App source ----
COPY backend/ /app/backend/
COPY skills/  /app/skills/
COPY 数据测试集/  /app/数据测试集/

# HF Spaces persistent storage opt-in (free tier: 20GB on CPU).
# This is where the SQLite DB lives between deploys. The app still pushes
# snapshots to a HF Dataset repo for off-host backup, so disk loss is non-fatal.
RUN mkdir -p /data /.cache/huggingface

# Ensure the data dir is writable by the runtime user (HF Spaces runs as
# user 1000 by default, not root).
RUN chown -R 1000:1000 /app /data /.cache/huggingface 2>/dev/null || true
USER 1000

WORKDIR /app/backend

EXPOSE 7860

# tini → forwards SIGTERM properly to uvicorn so the lifespan `shutdown`
# hook runs and we get a final HF push.
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command. $PORT is set by the Space runtime (defaults to 7860 above).
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1 --proxy-headers"]

# ---- Healthcheck (Space hardware uses this) ----
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:${PORT:-7860}/api/health || exit 1
