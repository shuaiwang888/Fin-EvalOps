"""SSE broker — in-memory pub/sub for run progress events.

Each Run gets its own async Queue keyed by run_id. The HTTP SSE endpoint
subscribes; the evaluator publishes step-by-step updates.

For Render single-worker deployments this in-process queue is sufficient.
If we later scale to multiple workers we'd swap to Redis pub/sub.
"""
from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import Any, AsyncIterator, Dict

from ..utils.trace import get_logger

log = get_logger(__name__)

_SENTINEL = object()


class SSEBroker:
    def __init__(self) -> None:
        self._channels: Dict[str, list[asyncio.Queue]] = defaultdict(list)

    def publish(self, channel: str, event: str, data: Any) -> None:
        """Send `data` to all subscribers of `channel`. Thread-safe."""
        payload = {"event": event, "data": data}
        for q in list(self._channels.get(channel, [])):
            try:
                q.put_nowait(payload)
            except asyncio.QueueFull:
                log.warning("SSE queue full for channel %s, dropping event", channel)

    def close(self, channel: str) -> None:
        for q in list(self._channels.get(channel, [])):
            try:
                q.put_nowait(_SENTINEL)
            except asyncio.QueueFull:
                pass
        self._channels.pop(channel, None)

    async def subscribe(self, channel: str) -> AsyncIterator[dict]:
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        self._channels[channel].append(q)
        try:
            while True:
                item = await q.get()
                if item is _SENTINEL:
                    break
                yield item
        finally:
            if q in self._channels.get(channel, []):
                self._channels[channel].remove(q)


# Module-level singleton
broker = SSEBroker()


def format_sse(event: str, data: Any) -> str:
    """Format a single SSE message."""
    payload = json.dumps(data, ensure_ascii=False, default=str)
    return f"event: {event}\ndata: {payload}\n\n"
