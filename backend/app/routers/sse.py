"""SSE router — live progress for individual runs and batches."""
from __future__ import annotations

import asyncio
from typing import AsyncIterator

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from ..services.sse_broker import broker

router = APIRouter()


async def _gen(channel: str, hello_payload: dict) -> AsyncIterator[dict]:
    yield {"event": "hello", "data": hello_payload}
    try:
        async for item in broker.subscribe(channel):
            yield {"event": item["event"], "data": item["data"]}
            if item["event"] in {"complete", "error"}:
                break
    except asyncio.CancelledError:
        pass


@router.get("/runs/{run_id}")
async def sse_run(run_id: str):
    return EventSourceResponse(
        _gen(f"runs/{run_id}", {"channel": "runs", "id": run_id}),
        ping=15,
    )


@router.get("/batches/{batch_id}")
async def sse_batch(batch_id: str):
    return EventSourceResponse(
        _gen(f"batches/{batch_id}", {"channel": "batches", "id": batch_id}),
        ping=15,
    )
