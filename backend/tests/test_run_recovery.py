from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models import Run, RunBatch
from app.services.run_recovery import reconcile_runs


def test_reconcile_marks_interrupted_and_fake_zero_but_preserves_real_zero():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as db:
        batch = RunBatch(id="batch", judge_model="m", judge_provider="p", total=4)
        db.add(batch)
        db.add_all([
            Run(
                id="pending", batch_id="batch", testcase_id="tc1", skill_id="s",
                judge_model="m", judge_provider="p", status="pending",
            ),
            Run(
                id="fake-zero", batch_id="batch", testcase_id="tc2", skill_id="s",
                judge_model="m", judge_provider="p", status="done", final_score=0,
                weight_assignment={}, dimension_scores={},
            ),
            Run(
                id="real-zero", batch_id="batch", testcase_id="tc3", skill_id="s",
                judge_model="m", judge_provider="p", status="done", final_score=0,
                weight_assignment={
                    "accuracy": {"dynamic_weight": 100, "applicability": "relevant"},
                },
                dimension_scores={"accuracy": {"raw_score": 0}},
            ),
            Run(
                id="repairable-zero", batch_id="batch", testcase_id="tc4", skill_id="s",
                judge_model="m", judge_provider="p", status="done", final_score=0,
                weight_assignment={
                    "dim_0": {"dynamic_weight": 60, "applicability": "relevant"},
                    "dim_1": {"dynamic_weight": 40, "applicability": "relevant"},
                },
                dimension_scores={
                    "accuracy": {"raw_score": 80},
                    "evidence": {"raw_score": 60},
                },
            ),
        ])
        db.commit()

        result = reconcile_runs(db)

        assert result == {"interrupted": 1, "invalid_zero": 1, "repaired_zero": 1}
        assert db.get(Run, "pending").status == "failed"
        assert "中断" in db.get(Run, "pending").error_msg
        assert db.get(Run, "fake-zero").status == "failed"
        assert db.get(Run, "fake-zero").final_score is None
        assert db.get(Run, "real-zero").status == "done"
        assert db.get(Run, "real-zero").final_score == 0
        assert db.get(Run, "repairable-zero").final_score == 72
        assert list(db.get(Run, "repairable-zero").weight_assignment) == ["accuracy", "evidence"]
        assert batch.done == 2
        assert batch.failed == 2
