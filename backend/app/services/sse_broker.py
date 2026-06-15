"""SSE broker — in-memory pub/sub for run progress events.

Each Run gets its own async Queue keyed by run_id. The HTTP SSE endpoint
subscribes; the evaluator publishes step-by-step updates.

For HF Space (Docker, single uvicorn worker) this in-process queue is
sufficient. If we later scale to multiple workers we'd swap to Redis pub/sub.
"""
from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, AsyncIterator, Dict, Set

from ..utils.trace import get_logger

log = get_logger(__name__)

_SENTINEL = object()


class SSEBroker:
    def __init__(self) -> None:
        self._channels: Dict[str, list[asyncio.Queue]] = defaultdict(list)
        # Channels that have been closed but still have subscribers draining
        # pending events. New subscribers should bail out immediately.
        self._closed: Set[str] = set()

    def is_closed(self, channel: str) -> bool:
        return channel in self._closed

    def publish(self, channel: str, event: str, data: Any) -> None:
        """Send `data` to all subscribers of `channel`. Thread-safe.

        No-op for closed channels.
        """
        if self.is_closed(channel):
            return
        payload = {"event": event, "data": data}
        for q in list(self._channels.get(channel, [])):
            try:
                q.put_nowait(payload)
            except asyncio.QueueFull:
                log.warning("SSE queue full for channel %s, dropping event", channel)

    def close(self, channel: str) -> None:
        """Mark channel closed, signal all current subscribers to drain, then
        forget the channel.

        New subscribers that call `subscribe()` after this will see
        `is_closed()` == True and bail out immediately.
        """
        self._closed.add(channel)
        for q in list(self._channels.get(channel, [])):
            try:
                q.put_nowait(_SENTINEL)
            except asyncio.QueueFull:
                pass
        self._channels.pop(channel, None)

    async def subscribe(self, channel: str) -> AsyncIterator[dict]:
        if self.is_closed(channel):
            # Channel already finished — don't open a queue that will never
            # receive events. The caller will see an empty stream and the
            # EventSourceResponse will close naturally.
            return
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        # Re-check: a concurrent close() between our is_closed() and append()
        # would leave a queue that never receives a sentinel. Guard:
        if self.is_closed(channel):
            return
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
