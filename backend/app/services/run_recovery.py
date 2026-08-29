"""Startup reconciliation for evaluation runs left in impossible states."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import Run, RunBatch
from ..utils.trace import get_logger

log = get_logger(__name__)

IN_FLIGHT = ("pending", "routing", "running", "scoring")


def reconcile_runs(db: Session) -> dict[str, int]:
    """Make interrupted and structurally invalid historical runs actionable.

    Background tasks cannot survive a process/container restart. Any in-flight
    row restored from persistence is therefore interrupted, not still running.
    Older releases also wrote empty judge payloads as done/0; reclassify only
    those empty-structure rows while preserving genuine explicit zero scores.
    """
    now = datetime.now(timezone.utc)
    interrupted = 0
    invalid_zero = 0

    for run in db.query(Run).filter(Run.status.in_(IN_FLIGHT)).all():
        run.status = "failed"
        run.current_step = "failed"
        run.finished_at = now
        run.error_msg = "服务重启或任务进程中断，未产生完整评测结果；请重新评测"
        interrupted += 1

    candidates = db.query(Run).filter(Run.status == "done", Run.final_score == 0).all()
    for run in candidates:
        if run.weight_assignment and run.dimension_scores:
            continue
        run.status = "failed"
        run.current_step = "failed"
        run.finished_at = run.finished_at or now
        run.error_msg = "历史 Judge 输出缺少权重或维度评分，原 0 分无效；请重新评测"
        run.final_score = None
        run.absolute_score_pre_cap = None
        invalid_zero += 1

    if interrupted or invalid_zero:
        _refresh_batch_counts(db)
        db.commit()
        log.warning(
            "Reconciled evaluation runs: interrupted=%d invalid_zero=%d",
            interrupted,
            invalid_zero,
        )
    return {"interrupted": interrupted, "invalid_zero": invalid_zero}


def _refresh_batch_counts(db: Session) -> None:
    for batch in db.query(RunBatch).all():
        statuses = [
            status
            for (status,) in db.query(Run.status).filter(Run.batch_id == batch.id)
        ]
        batch.done = sum(status == "done" for status in statuses)
        batch.failed = sum(status in {"failed", "cancelled"} for status in statuses)
