"""
Test Suite for Health Endpoint.
Required: GET /health returns {"status": "ok"}
"""

from fastapi.testclient import TestClient


def test_root_health_endpoint(client: TestClient) -> None:
    """Asserts that GET /health returns status 200 and {'status': 'ok'}."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_api_v1_health_endpoint(client: TestClient) -> None:
    """Asserts that GET /api/v1/health returns status 200 and {'status': 'ok'}."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
