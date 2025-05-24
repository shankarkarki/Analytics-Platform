"""
Basic test for the main module.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] ==  "Welcome to the FastAPI Event Analytics Platform! version 1.0.0"
    assert "version" in data["message"]

def test_create_event():
    event_data = {
        "user_id": "user123",
        "event_name": "test_event",
        "event_properties": {"browser": "chrome","page": "/login"},
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Event created successfully"
    assert "event_id" in data

def test_get_events():

    event_data = {
        "user_id": "user123",
        "event_name": "test_event",
        "event_properties": {"page": "dashboard"},
    }
    response = client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data
    assert "events" in data

def test_get_analytics_summary():
    response = client.get("/analytics/summary/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "total_events" in data
    assert "unique_users" in data
    assert "events_type" in data
