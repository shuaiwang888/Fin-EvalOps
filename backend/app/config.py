"""Application settings loaded from environment variables.

All sensitive values (LLM keys, internal URLs) must be supplied via env vars
or `.env` file. Defaults below are placeholders only and never include real
secrets.

NOTE on env-read semantics
--------------------------
The pydantic ``Settings`` instance is created once at module import time and
its values are then frozen. If an operator edits HF Space Variables / Secrets
later, the running Python process keeps the *original* empty values. This
bit us once on the HF Space (Space Secrets showed as "configured" in the
admin endpoint, but ``available_providers`` returned an empty list).

To make config hot-reload safe, every field that the operator might want to
edit *after* the process is running is exposed as a ``@property`` that reads
``os.environ`` on every call. Plain fields (paths, log level) keep the
pydantic behaviour because they never change at runtime.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _env(name: str, default: str = "") -> str:
    """Read an env var live. Used by the ``*_live`` properties below."""
    v = os.environ.get(name)
    if v:
        return v
    # Fall back to the pydantic-cached value (captured at import time) when
    # the env var is unset — keeps local dev with a .env file working.
    try:
        cached = getattr(_settings, name.lower(), None)
        if cached:
            return cached
    except Exception:
        pass
    return default


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----- LLM providers (initial values only — see *_live properties) -----
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    dashscope_api_key: str = ""
    deepseek_api_key: str = ""
    # MiniMax — Anthropic-compatible endpoint exposed at /anthropic path
    minimax_api_key: str = ""
    minimax_base_url: str = "https://api.minimaxi.com/anthropic"

    # ----- Internal services -----
    iwencai_base_url: str = ""
    iwencai_verify_ssl: bool = False

    # ----- Paths (not env-driven in practice) -----
    skills_root: str = "../skills"
    testsets_root: str = "../自研评测测试集"
    db_path: str = "./data/fin_evalops.db"

    # ----- Web -----
    cors_origins: str = "http://localhost:5173,https://shuaiwang888.github.io"
    default_judge_model: str = "minimax-3"

    # ----- HF persistence (Dataset repo for SQLite) -----
    hf_token: str = ""
    hf_namespace: str = ""
    hf_dataset_repo: str = "fin-evalops-db"
    hf_push_interval: int = 300

    # Protect destructive/operational admin mutations exposed by the API.
    # Read-only health and persistence status remain public.
    admin_api_token: str = ""

    # ----- Misc -----
    log_level: str = "INFO"

    # Max concurrent eval jobs inside a single batch (ThreadPoolExecutor in
    # services/evaluator.py). 3 is conservative for free-tier LLM keys.
    eval_batch_concurrency: int = 3

    @field_validator("skills_root", "testsets_root", "db_path", mode="before")
    @classmethod
    def _expand(cls, v: str) -> str:
        if not v:
            return v
        return str(Path(v).expanduser())

    # ------------------------------------------------------------------------
    # Live env properties — these read os.environ on EVERY access, so
    # editing HF Space Variables / Secrets at runtime takes effect
    # immediately without restarting the Python process.
    # ------------------------------------------------------------------------
    @property
    def anthropic_api_key_live(self) -> str:  return _env("ANTHROPIC_API_KEY")
    @property
    def openai_api_key_live(self) -> str:      return _env("OPENAI_API_KEY")
    @property
    def dashscope_api_key_live(self) -> str:   return _env("DASHSCOPE_API_KEY")
    @property
    def deepseek_api_key_live(self) -> str:    return _env("DEEPSEEK_API_KEY")
    @property
    def minimax_api_key_live(self) -> str:     return _env("MINIMAX_API_KEY")
    @property
    def minimax_base_url_live(self) -> str:    return _env("MINIMAX_BASE_URL", self.minimax_base_url)
    @property
    def hf_token_live(self) -> str:            return _env("HF_TOKEN")
    @property
    def hf_namespace_live(self) -> str:        return _env("HF_NAMESPACE")
    @property
    def hf_dataset_repo_live(self) -> str:     return _env("HF_DATASET_REPO", self.hf_dataset_repo)
    @property
    def hf_push_interval_live(self) -> int:
        try: return int(_env("HF_PUSH_INTERVAL", str(self.hf_push_interval)))
        except ValueError: return self.hf_push_interval
    @property
    def cors_origins_live(self) -> str:        return _env("CORS_ORIGINS", self.cors_origins)
    @property
    def default_judge_model_live(self) -> str: return _env("DEFAULT_JUDGE_MODEL", self.default_judge_model)
    @property
    def iwencai_base_url_live(self) -> str:    return _env("IWENCAI_BASE_URL")
    @property
    def admin_api_token_live(self) -> str:     return _env("ADMIN_API_TOKEN")
    @property
    def iwencai_verify_ssl_live(self) -> bool:
        v = os.environ.get("IWENCAI_VERIFY_SSL", "").lower()
        if v in ("1", "true", "yes", "on"):
            return True
        if v in ("0", "false", "no", "off"):
            return False
        return self.iwencai_verify_ssl

    # ------------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------------
    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins_live.split(",") if o.strip()]

    @property
    def project_root(self) -> Path:
        """Absolute path to the Fin-EvalOps root (one level above backend/)."""
        return Path(__file__).resolve().parents[2]

    @property
    def skills_root_abs(self) -> Path:
        p = Path(self.skills_root)
        return (p if p.is_absolute() else (Path(__file__).resolve().parents[1] / p)).resolve()

    @property
    def testsets_root_abs(self) -> Path:
        p = Path(self.testsets_root)
        return (p if p.is_absolute() else (Path(__file__).resolve().parents[1] / p)).resolve()

    @property
    def db_path_abs(self) -> Path:
        p = Path(self.db_path)
        return (p if p.is_absolute() else (Path(__file__).resolve().parents[1] / p)).resolve()

    @property
    def available_providers(self) -> List[str]:
        out = []
        if self.anthropic_api_key_live: out.append("anthropic")
        if self.openai_api_key_live:     out.append("openai")
        if self.dashscope_api_key_live:  out.append("dashscope")
        if self.deepseek_api_key_live:   out.append("deepseek")
        if self.minimax_api_key_live:    out.append("minimax")
        return out

    @property
    def hf_configured(self) -> bool:
        return bool(self.hf_token_live) and bool(self.hf_namespace_live) and bool(self.hf_dataset_repo_live)

    # ------------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------------
    def env_diagnostics(self) -> dict:
        """Return which env-driven settings are actually set RIGHT NOW.
        Used by the /api/admin/diagnose endpoint to debug Space config issues."""
        keys = [
            "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "DASHSCOPE_API_KEY",
            "DEEPSEEK_API_KEY", "MINIMAX_API_KEY", "MINIMAX_BASE_URL",
            "HF_TOKEN", "HF_NAMESPACE", "HF_DATASET_REPO", "HF_PUSH_INTERVAL",
            "CORS_ORIGINS", "DEFAULT_JUDGE_MODEL", "IWENCAI_BASE_URL",
            "IWENCAI_VERIFY_SSL", "ADMIN_API_TOKEN",
        ]
        out: dict = {}
        for k in keys:
            v = os.environ.get(k)
            if v:
                if "KEY" in k or "TOKEN" in k:
                    # This payload is exposed by a read-only diagnostics endpoint.
                    # Even a short prefix is unnecessary secret material, so only
                    # report presence and length.
                    out[k] = f"set ({len(v)} chars)"
                else:
                    out[k] = v
            else:
                out[k] = None
        return out


_settings = Settings()  # captured singleton for the `_env()` fallback
settings = _settings    # canonical name used throughout the codebase
