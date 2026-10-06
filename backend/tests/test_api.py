from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_and_status_endpoints():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}

    response = client.get("/api/system/status")
    assert response.status_code == 200
    assert "camera" in response.json()


def test_zone_api_and_metrics():
    response = client.get("/api/zones")
    assert response.status_code == 200

    response = client.get("/api/metrics")
    assert response.status_code == 200
    assert "fps" in response.json()
