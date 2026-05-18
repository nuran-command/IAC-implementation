import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
if "main" in sys.modules:
    del sys.modules["main"]

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Payment/Cost Estimator"
    assert "cost_per_point" in response.json()

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_read_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "payment_service_status" in response.text
