from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


def test_admin_persistence_mutations_require_token(monkeypatch):
    monkeypatch.setenv("ADMIN_API_TOKEN", "test-admin-secret")
    client = TestClient(app)

    missing = client.post("/api/admin/persistence/push")
    assert missing.status_code == 401

    wrong = client.post(
        "/api/admin/persistence/pull",
        headers={"X-Admin-Token": "wrong"},
    )
    assert wrong.status_code == 401


def test_admin_mutations_are_disabled_without_server_token(monkeypatch):
    monkeypatch.delenv("ADMIN_API_TOKEN", raising=False)
    from app.config import settings

    monkeypatch.setattr(settings, "admin_api_token", "")
    client = TestClient(app)
    response = client.post("/api/admin/persistence/push")
    assert response.status_code == 503


def test_diagnostics_never_expose_secret_prefix(monkeypatch):
    secret = "private-token-value"
    monkeypatch.setenv("ADMIN_API_TOKEN", secret)

    diagnostics = settings.env_diagnostics()

    assert diagnostics["ADMIN_API_TOKEN"] == f"set ({len(secret)} chars)"
    assert secret[:6] not in diagnostics["ADMIN_API_TOKEN"]
