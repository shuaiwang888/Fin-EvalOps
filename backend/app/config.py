"""Application settings loaded from environment variables.

All sensitive values (LLM keys, internal URLs) must be supplied via env vars
or `.env` file. Defaults below are placeholders only and never include real
secrets.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----- LLM providers (read-only in app, never exposed via API) -----
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    dashscope_api_key: str = ""
    deepseek_api_key: str = ""

    # ----- Internal services -----
    iwencai_base_url: str = ""
    iwencai_verify_ssl: bool = False

    # ----- Paths -----
    skills_root: str = "../"
    testsets_root: str = "../数据测试集"
    db_path: str = "./data/fin_evalops.db"

    # ----- Web -----
    cors_origins: str = "http://localhost:5173"
    default_judge_model: str = "claude-sonnet-4-6"

    # ----- Misc -----
    log_level: str = "INFO"

    @field_validator("skills_root", "testsets_root", "db_path", mode="before")
    @classmethod
    def _expand(cls, v: str) -> str:
        if not v:
            return v
        return str(Path(v).expanduser())

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def project_root(self) -> Path:
        """Absolute path to the Fin-EvalOps root (one level above backend/)."""
        # config.py is in backend/app/, so go up 2
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
        if self.anthropic_api_key:
            out.append("anthropic")
        if self.openai_api_key:
            out.append("openai")
        if self.dashscope_api_key:
            out.append("dashscope")
        if self.deepseek_api_key:
            out.append("deepseek")
        return out


settings = Settings()
