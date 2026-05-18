import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
if "main" in sys.modules:
    del sys.modules["main"]

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root_healthy():
    if "DB_HOST" in os.environ:
        del os.environ["DB_HOST"]
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Order/Board Manager"
    assert "tasks" in response.json()

def test_read_health_healthy():
    if "DB_HOST" in os.environ:
        del os.environ["DB_HOST"]
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_read_metrics_healthy():
    if "DB_HOST" in os.environ:
        del os.environ["DB_HOST"]
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "order_service_status 1" in response.text

def test_read_root_unhealthy(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db_wrong")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "offline"
    assert "Database connection failed" in response.json()["error"]

def test_read_health_unhealthy(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db_wrong")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "unhealthy"
    assert "Database connection failed" in response.json()["error"]

def test_read_metrics_unhealthy(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db_wrong")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "order_service_status 0" in response.text
