"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
import secrets
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from . import __version__
from .config import settings
from .db import DATABASE_URL, init_db
from .routers import agent, annotations, dashboard, runs, skills, sse, testsets
from .schemas import HealthResponse
from .services.skill_loader import SkillLoader
from .utils.trace import get_logger, setup_logging

# Imported lazily inside lifespan to avoid import-time cost when the app is
# reloaded (e.g. by uvicorn --reload or pytest).
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    setup_logging(settings.log_level)
    log.info("Starting Fin-EvalOps backend v%s", __version__)
    log.info("DB: %s", DATABASE_URL)
    log.info("Skills root: %s", settings.skills_root_abs)
    log.info("Testsets root: %s", settings.testsets_root_abs)
    log.info("Available LLM providers: %s", settings.available_providers or "<none>")
    log.info("Default judge: %s", settings.default_judge_model_live)
    log.info("HF persistence: %s", "enabled" if settings.hf_configured else "disabled (local-only)")

    # ---- 1) Pull latest DB from HF Dataset (if configured + local is empty) ----
    try:
        from . import persistence
        if persistence.pull_db():
            log.info("Restored DB from HF Dataset repo")
    except Exception as exc:
        log.exception("HF pull at startup failed (non-fatal): %s", exc)

    # ---- 2) Ensure schema exists (no-op if tables already present) ----
    init_db()

    # ---- 3) Warm Skill cache so first /api/skills request is fast ----
    try:
        loader = SkillLoader(settings.skills_root_abs)
        n = loader.sync_to_db()
        log.info("Synced %d skills into DB", n)
    except Exception as exc:
        log.exception("Skill auto-sync failed (non-fatal): %s", exc)

    # ---- 4) Reconcile jobs that could not survive a previous restart ----
    try:
        from .db import db_session
        from .services.run_recovery import reconcile_runs
        with db_session() as db:
            recovered = reconcile_runs(db)
        if any(recovered.values()):
            from . import persistence
            persistence.mark_dirty()
    except Exception as exc:
        log.exception("Run reconciliation failed (non-fatal): %s", exc)

    # ---- 5) Start background HF pusher (debounced DB uploads) ----
    try:
        from . import persistence
        persistence.start_pusher()
    except Exception as exc:
        log.exception("HF pusher start failed (non-fatal): %s", exc)

    yield

    # ---- Shutdown: stop pusher + final push (captures in-progress writes) ----
    log.info("Shutdown: flushing DB to HF (if configured)")
    try:
        from . import persistence
        persistence.stop_pusher(timeout=5.0)
        persistence.push_db(reason="shutdown", force=True)
    except Exception as exc:
        log.exception("HF push on shutdown failed (non-fatal): %s", exc)
    log.info("Shutdown complete.")


app = FastAPI(
    title="Fin-EvalOps API",
    version=__version__,
    description="13 类自研评测 Skill × 多模型 Judge × Web 评测平台",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    # The app uses header/token based requests and no cross-site cookies.
    # Keeping this false also makes the wildcard development fallback valid.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Run-Id", "X-Batch-Id"],
)


@app.middleware("http")
async def prevent_dynamic_response_caching(request: Request, call_next) -> Response:
    """Prevent browsers/proxies from persisting transient HF edge error pages.

    HF Spaces can briefly serve a 404 HTML placeholder while the container is
    waking or restarting. If that placeholder is cached for an API URL, the
    frontend keeps seeing the stale HTML even after FastAPI is healthy again.
    """
    response: Response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith(("/api", "/docs", "/openapi.json", "/redoc")):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# ---------------------- Health ----------------------
@app.get("/", tags=["meta"])
def root() -> dict:
    return {
        "name": "Fin-EvalOps",
        "version": __version__,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    return HealthResponse(
        version=__version__,
        providers=settings.available_providers,
        db="connected",
    )


@app.get("/api/admin/persistence", tags=["meta"])
def persistence_status() -> dict:
    """Cheap endpoint to inspect HF persistence state (used by the deploy doc
    and for smoke-testing on the Space)."""
    from pathlib import Path
    from . import persistence
    local = Path(settings.db_path_abs)
    return {
        "hf_configured": settings.hf_configured,
        "hf_namespace": settings.hf_namespace_live,
        "hf_dataset_repo": settings.hf_dataset_repo_live,
        "hf_push_interval_seconds": settings.hf_push_interval_live,
        "dirty": persistence.is_dirty(),
        "local_db_bytes": local.stat().st_size if local.exists() else 0,
    }


@app.get("/api/admin/diagnose", tags=["meta"])
def diagnose() -> dict:
    """Read every env-driven setting live and report what's set.

    Use this when an admin endpoint shows one thing but the live app behaves
    differently — e.g. Settings shows 0 models but a key is in the dashboard.
    Secret-shaped values report presence and length only; no value fragment is exposed.
    """
    from . import persistence
    return {
        "env": settings.env_diagnostics(),
        "available_providers": settings.available_providers,
        "default_judge_model": settings.default_judge_model_live,
        "cors_origins": settings.cors_origins_list,
        "hf_configured": settings.hf_configured,
        "models": _models_snapshot(),
    }


def _models_snapshot() -> list[dict]:
    """Return the registry view the way `list_models()` would see it now."""
    from .services.llm_client import MODELS
    out = []
    for m in MODELS.values():
        key_attr = f"{m.provider}_api_key_live"
        has_key = bool(getattr(settings, key_attr, ""))
        out.append({
            "id": m.id,
            "provider": m.provider,
            "label": m.label,
            "context_window": m.context_window,
            "has_api_key": has_key,
        })
    return out


def _require_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    expected = settings.admin_api_token_live
    if not expected:
        raise HTTPException(503, "ADMIN_API_TOKEN is not configured; admin mutations are disabled")
    if not x_admin_token or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(401, "Invalid admin token")


@app.post("/api/admin/persistence/push", tags=["meta"])
def persistence_force_push(_: None = Depends(_require_admin_token)) -> dict:
    """Force an immediate push of the current DB to HF (bypasses dirty flag).
    Useful after manual edits or for one-off snapshots."""
    from . import persistence
    ok = persistence.push_db(reason="manual-api", force=True)
    return {"ok": ok}


@app.post("/api/admin/persistence/pull", tags=["meta"])
def persistence_force_pull(_: None = Depends(_require_admin_token)) -> dict:
    """Force a pull from HF (overwrites local DB). Destructive."""
    from . import persistence
    ok = persistence.pull_db(force=True)
    return {"ok": ok}


# ---------------------- Routers ----------------------
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(testsets.router, prefix="/api/testsets", tags=["testsets"])
app.include_router(runs.router, prefix="/api", tags=["runs"])  # mounts /runs and /route
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["annotations"])
app.include_router(sse.router, prefix="/api/sse", tags=["sse"])
