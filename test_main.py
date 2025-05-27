"""
Basic test for the main module.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database import get_session
from models import EventCreate

# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_session():
    """Override the get_session dependency for testing"""
    async with TestSessionLocal() as session:
        yield session

# Override the dependency in the FastAPI app
app.dependency_overrides[get_session] = override_get_session


client = TestClient(app)

@pytest_asyncio.fixture(scope="function")
async def setup_database():
    """Fixture to set up the test database"""
    async with test_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        # Drop all tables after tests
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio
async def test_create_event(setup_database):
    """Test creating an event"""
    event_data = {
        "user_id": "user123",
        "event_name": "test_event",
        "session id" : "session123",
        "event_properties": {"browser": "chrome", "page": "/login"},
        "user_properties": {"age": 30, "country": "US"},
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Event created successfully"
    assert "event_id" in data  
    assert "timestamp" in data     

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] ==  "Welcome to the FastAPI Event Analytics Platform! version 1.0.0"
    assert "version" in data["message"]


@pytest.mark.asyncio
async def test_get_events(setup_database):
    """Test getting events from database"""

    #create events first

    for i in range(3):
        event_data = {
            "user_id": f"user{i}",
            "event_name": f"test_event_{i}",
            "session_id": f"session{i}",
            "properties": {"page": f"/page_{i}"},  
        }

    response = client.post("/events/", json=event_data)

# then get the events
    response = client.get("/events/?limit=5&offset=0")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_events"] == 3
    assert len(data["events"]) == 3
    assert data["limits"] == 5
    assert data["offset"] == 0
    assert "total_events" in data
    assert "events" in data


@pytest.mark.asyncio
async def test_get_analytics_summary(setup_database):
    """Test getting analytics summary""" 
    # Create some events first

    for i in range(5):
        test_event_data = {
            "user_id": f"user{i}",
            "event_name": f"test_event_{i}",
            "session_id": f"session{i}",
        }

    for event in test_event_data:
        client.post("/events/", json=event)

    # Now get the analytics summary

    response = client.get("/analytics/summary/")
    assert response.status_code == 200
    
    
    data = response.json()
    assert data["total_events"] == 5
    assert data["unique_users"] == 5
    assert data["unique_sessions"] == 5
    assert "data_range" in data

