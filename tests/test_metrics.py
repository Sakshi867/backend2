import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import date

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DaySense AI API is running" in response.json()["message"]

def test_create_daily_metrics_unauthorized():
    # Test without auth token
    payload = {
        "timestamp": str(date.today()),
        "screen_minutes_social": 10.5,
        "screen_minutes_productivity": 30.0,
        "screen_minutes_entertainment": 15.0,
        "continuous_screen_minutes": 20.0,
        "app_switch_count": 5,
        "night_usage_minutes": 0.0,
        "step_count": 5000,
        "active_minutes": 45.0,
        "screen_break_minutes": 10.0,
        "morning_activity_minutes": 20.0,
        "task_deep_minutes": 120.0,
        "task_light_minutes": 60.0,
        "task_switch_count": 10
    }
    response = client.post("/api/metrics/daily", json=payload)
    assert response.status_code == 403 # HTTPBearer returns 403 when no credentials provided

def test_create_daily_metrics_mock_auth():
    # For testing, we might need a way to bypass or mock the verify_firebase_token dependency
    # This is a basic test case structure.
    pass
