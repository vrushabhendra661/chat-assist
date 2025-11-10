"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
from database import Base, engine

# Create test client
client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    """Test root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


@patch("chat_service.ChatService.generate_response", new_callable=AsyncMock)
def test_chat_endpoint_success(mock_generate, setup_database):
    """Test successful chat request"""
    mock_generate.return_value = "Hello! How can I help you today?"
    
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "session_id": "test_session"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == "test_session"


@patch("chat_service.ChatService.generate_response", new_callable=AsyncMock)
def test_chat_endpoint_default_session(mock_generate, setup_database):
    """Test chat request with default session"""
    mock_generate.return_value = "I'm doing great!"
    
    response = client.post(
        "/api/chat",
        json={"message": "How are you?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "default"


@patch("chat_service.ChatService.generate_response", new_callable=AsyncMock)
def test_chat_endpoint_error(mock_generate, setup_database):
    """Test chat endpoint error handling"""
    mock_generate.side_effect = Exception("API Error")
    
    response = client.post(
        "/api/chat",
        json={"message": "Test message"}
    )
    
    assert response.status_code == 500


def test_clear_session():
    """Test clearing session context"""
    response = client.post(
        "/api/clear",
        json={"session_id": "test_session"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_get_history(setup_database):
    """Test retrieving chat history"""
    # First, create some chat history
    client.post(
        "/api/chat",
        json={"message": "Test message", "session_id": "history_test"}
    )
    
    response = client.get("/api/history/history_test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_history_with_limit(setup_database):
    """Test retrieving chat history with limit"""
    response = client.get("/api/history/test_session?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_chat_endpoint_missing_message():
    """Test chat endpoint with missing message"""
    response = client.post("/api/chat", json={})
    assert response.status_code == 422  # Validation error

