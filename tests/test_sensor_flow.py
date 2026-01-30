import os
import pytest
from datetime import datetime, timezone
import json
from unittest.mock import AsyncMock, patch, MagicMock

# Mock environment variables for DB - needs to happen before imports if possible, 
# or we need to reload the module. But since it worked for DB, we keep it.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["FIREBASE_PROJECT_ID"] = "test-project"

from fastapi.testclient import TestClient
from main import app
from database import Base, engine
from security import get_current_user

# 1. Override Authentication
app.dependency_overrides[get_current_user] = lambda: "mock-user-id"

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)

def test_ingest_sensor_data():
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data_type": "accelerometer",
        "payload": {"x": 1.0, "y": 0.5, "z": 0.1}
    }
    # No Authorization header needed because we overrode the dependency
    response = client.post("/api/metrics/sensor", json=payload)
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_id"] == "mock-user-id"
    assert data["data_type"] == "accelerometer"
    assert "id" in data

@patch("sensor_service.httpx.AsyncClient")
def test_aggregate_and_forward(mock_client_cls):
    # Create the mock client instance
    mock_client = AsyncMock()
    # When httpx.AsyncClient() is called, return this mock
    mock_client_cls.return_value = mock_client
    
    # Setup context manager return
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    # Setup the post method on the mock instance
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    
    # client.post() is async, so it returns a coroutine that resolves to response
    mock_client.post.return_value = mock_response

    response = client.post("/api/metrics/aggregate")
    
    print(response.text) # For debugging if it fails
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "success"
    
    # Verify we tried to call Backend3
    mock_client.post.assert_called()
    call_args = mock_client.post.call_args
    # call_args[0][0] is the url
    assert "http://localhost:8001/api/energy/update" in call_args[0][0]
    
    # Checking payload
    sent_payload = call_args[1]["json"]
    assert sent_payload["user_id"] == "mock-user-id"
    assert "metrics" in sent_payload
