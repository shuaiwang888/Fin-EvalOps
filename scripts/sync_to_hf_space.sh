#!/usr/bin/env bash
# sync_to_hf_space.sh — push current main branch to the Fin-EvalOps-v2 HF Space.
#
# Usage:
#   1. Open https://huggingface.co/settings/tokens and make sure you have a
#      token with write access to the appqqq/Fin-EvalOps-v2 Space.
#   2. Either:
#        - log in once:    huggingface-cli login   (pastes the token)
#      OR
#        - export HF_TOKEN before running this script.
#   3. From the Fin-EvalOps repo root:  bash scripts/sync_to_hf_space.sh
#
# What it does:
#   - clones https://huggingface.co/spaces/appqqq/Fin-EvalOps-v2 into
#     /tmp/hf-space-finevalops-v2 (re-uses if already present)
#   - rsyncs the current working tree in (excluding frontend, local DB,
#     caches, .git, .github)
#   - commits + pushes; HF will auto-rebuild the Docker image

set -euo pipefail

REPO="/Users/appstore/AI-Code/Fin-EvalOps"
SPACE_URL="https://huggingface.co/spaces/appqqq/Fin-EvalOps-v2"
WORK="/tmp/hf-space-finevalops-v2"

cd "$REPO"

# Sanity: must be on main and clean (no uncommitted changes)
branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$branch" != "main" ]; then
  echo "❌ current branch is '$branch', expected 'main'." >&2
  exit 1
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ uncommitted local changes — commit or stash first." >&2
  exit 1
fi

short_sha="$(git rev-parse --short HEAD)"
short_msg="$(git log -1 --pretty=%s)"

# Auth: huggingface-cli login (preferred) OR HF_TOKEN env var
if [ -z "${HF_TOKEN:-}" ] && ! huggingface-cli whoami >/dev/null 2>&1; then
  echo "❌ not logged in. Run: huggingface-cli login" >&2
  echo "   or: export HF_TOKEN=hf_xxx..." >&2
  exit 1
fi

# Clone (shallow) if not present
if [ ! -d "$WORK/.git" ]; then
  echo "📥 cloning HF Space..."
  # Use the token for auth if provided (avoids the password prompt)
  if [ -n "${HF_TOKEN:-}" ]; then
    git clone "https://oauth2:${HF_TOKEN}@huggingface.co/spaces/appqqq/Fin-EvalOps-v2" "$WORK"
  else
    git clone "$SPACE_URL" "$WORK"
  fi
else
  echo "♻️  reusing existing clone at $WORK"
  git -C "$WORK" fetch origin
  git -C "$WORK" reset --hard origin/main
fi

# Rsync current code in (exclude things that should NOT be on the Space).
# Test data sources are uploaded via the web UI, NOT shipped in the image.
echo "📦 syncing files..."
rsync -a --delete \
      --exclude='.git' \
      --exclude='frontend' \
      --exclude='.pytest_cache' \
      --exclude='__pycache__' \
      --exclude='backend/data' \
      --exclude='.github' \
      --exclude='logs' \
      --exclude='*.pyc' \
      --exclude='数据测试集/' \
      --exclude='*.jsonl' \
      --exclude='_smoke_*.json' \
      "$REPO/" "$WORK/"

# Drop the local-only smoke-test fixture (11 MB) from the Space tree
rm -f "$WORK/数据测试集/_smoke_single.json"

cd "$WORK"

# Commit only if there are actual changes
if git diff --quiet HEAD; then
  echo "✅ HF Space is already up-to-date with $short_sha ($short_msg)"
else
  git add -A
  git -c user.name="claude-sync" -c user.email="noreply@anthropic.com" \
      commit -m "sync from GitHub: ${short_sha} ${short_msg}"
  echo "🚀 pushing to HF Space (triggers Docker rebuild, ~5-15 min)..."
  git push origin main
fi

echo ""
echo "🔍 Verify after rebuild (poll until POST appears):"
cat <<'EOF'
  HF="https://appqqq-fin-evalops-v2.hf.space"
  for i in $(seq 1 60); do
    methods=$(curl -s "$HF/openapi.json" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print([m.upper() for m in d['paths'].get('/api/testsets/categories',{})])")
    if echo "$methods" | grep -q POST; then
      echo "  ✅ ready after ${i}*15s: $methods"
      exit 0
    fi
    echo "  t=${i}*15s  methods=$methods  (waiting...)"
    sleep 15
  done
  echo "  ⚠️  still waiting after 15 min — check HF Space build logs."
EOF