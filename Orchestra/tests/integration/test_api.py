from fastapi.testclient import TestClient

from research_orchestrator.core.config import Settings
from research_orchestrator.main import create_app


def test_health_endpoint() -> None:
    app = create_app(Settings(app_env="test", llm_provider="deterministic", api_key=None))
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_contains_research_endpoint() -> None:
    app = create_app(Settings(app_env="test", llm_provider="deterministic", api_key=None))
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/v1/research-runs" in response.json()["paths"]

