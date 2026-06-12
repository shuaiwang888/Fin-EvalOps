"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from . import __version__
from .config import settings
from .db import DATABASE_URL, init_db
from .routers import agent, annotations, dashboard, runs, skills, sse, testsets
from .schemas import HealthResponse
from .services.skill_loader import SkillLoader
from .utils.trace import get_logger, setup_logging

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    setup_logging(settings.log_level)
    log.info("Starting Fin-EvalOps backend v%s", __version__)
    log.info("DB: %s", DATABASE_URL)
    log.info("Skills root: %s", settings.skills_root_abs)
    log.info("Testsets root: %s", settings.testsets_root_abs)
    log.info("Available LLM providers: %s", settings.available_providers or "<none>")

    init_db()
    # Warm Skill cache so first /api/skills request is fast
    try:
        loader = SkillLoader(settings.skills_root_abs)
        n = loader.sync_to_db()
        log.info("Synced %d skills into DB", n)
    except Exception as exc:
        log.exception("Skill auto-sync failed (non-fatal): %s", exc)

    yield
    log.info("Shutdown.")


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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Run-Id", "X-Batch-Id"],
)


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


# ---------------------- Routers ----------------------
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(testsets.router, prefix="/api/testsets", tags=["testsets"])
app.include_router(runs.router, prefix="/api", tags=["runs"])  # mounts /runs and /route
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["annotations"])
app.include_router(sse.router, prefix="/api/sse", tags=["sse"])
