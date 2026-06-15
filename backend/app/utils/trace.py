"""Lightweight structured logger.

Uses stdlib logging with a consistent prefix so the HF Space Logs pane stays
readable. Adds `trace_id` context for evaluator runs.
"""
from __future__ import annotations

import logging
import sys
from contextvars import ContextVar

_trace_id: ContextVar[str] = ContextVar("trace_id", default="-")


class _ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        record.trace_id = _trace_id.get()
        return True


_FMT = "%(asctime)s [%(levelname)s] [%(trace_id)s] %(name)s · %(message)s"


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_FMT))
    handler.addFilter(_ContextFilter())

    root = logging.getLogger()
    root.setLevel(level.upper())
    # avoid double-handlers on reload
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)

    # Mute noisy third-party loggers
    for name in ("httpx", "httpcore", "anthropic", "openai", "urllib3"):
        logging.getLogger(name).setLevel(logging.WARNING)


def set_trace_id(trace: str) -> None:
    _trace_id.set(trace)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
