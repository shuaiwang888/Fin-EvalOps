from __future__ import annotations


def test_stop_pusher_is_safe_when_never_started(monkeypatch):
    from app import persistence

    monkeypatch.setattr(persistence, "_pusher_thread", None)
    persistence.stop_pusher(timeout=0)
    assert persistence._pusher_thread is None
