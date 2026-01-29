import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date
from database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Only run for testing environment
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine) # Optional: cleanup

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DaySense AI API is running" in response.json()["message"]

def test_create_daily_metrics_unauthorized():
    payload = {
        "date": str(date.today()),
        "screen_time": 120.0,
        "tasks_completed": 5
    }
    response = client.post("/api/metrics/daily", json=payload)
    assert response.status_code == 401

def test_create_daily_metrics_mock_auth():
    # Note: security.py handles mock-user-id when ENVIRONMENT=testing
    payload = {
        "date": str(date.today()),
        "screen_time": 100.0,
        "tasks_completed": 3
    }
    headers = {"Authorization": "Bearer mock-token"}
    response = client.post("/api/metrics/daily", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "mock-user-id"
    assert data["screen_time"] == 100.0
    assert "energy_score" in data
    assert data["energy_level"] in ["LOW", "MEDIUM", "HIGH"]

def test_idempotency_upsert():
    headers = {"Authorization": "Bearer mock-token"}
    today = str(date.today())
    
    # First request
    payload1 = {"date": today, "screen_time": 50.0, "tasks_completed": 1}
    client.post("/api/metrics/daily", json=payload1, headers=headers)
    
    # Second request (update)
    payload2 = {"date": today, "screen_time": 200.0, "tasks_completed": 10}
    response = client.post("/api/metrics/daily", json=payload2, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["screen_time"] == 200.0
    assert data["tasks_completed"] == 10
