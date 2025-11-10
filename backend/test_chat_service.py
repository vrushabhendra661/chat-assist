"""
Unit tests for chat service
"""
import pytest
from unittest.mock import Mock, patch
from chat_service import ChatService


@pytest.fixture
def chat_service():
    """Create chat service instance for testing"""
    return ChatService()


@pytest.mark.asyncio
@patch("openai.OpenAI")
async def test_generate_response_new_session(mock_openai, chat_service):
    """Test generating response for new session"""
    # Mock OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    chat_service.client = mock_client
    
    # Generate response
    response = await chat_service.generate_response(
        message="Hello",
        session_id="test_session"
    )
    
    assert response == "Hello! How can I help you?"
    assert "test_session" in chat_service.contexts
    assert len(chat_service.contexts["test_session"]) == 2  # User + assistant


@pytest.mark.asyncio
@patch("openai.OpenAI")
async def test_generate_response_existing_session(mock_openai, chat_service):
    """Test generating response with existing context"""
    # Setup existing context
    chat_service.contexts["test_session"] = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    # Mock OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "I'm doing great!"
    
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    chat_service.client = mock_client
    
    # Generate response
    response = await chat_service.generate_response(
        message="How are you?",
        session_id="test_session"
    )
    
    assert response == "I'm doing great!"
    assert len(chat_service.contexts["test_session"]) == 4  # Previous 2 + new 2


@pytest.mark.asyncio
async def test_generate_response_context_limit(chat_service):
    """Test context limiting to prevent overflow"""
    # Set small context limit
    chat_service.max_context_messages = 4
    
    # Add many messages to exceed limit
    chat_service.contexts["test_session"] = [
        {"role": "user", "content": f"Message {i}"}
        for i in range(10)
    ]
    
    # Mock OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Response"
    
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    chat_service.client = mock_client
    
    await chat_service.generate_response(
        message="New message",
        session_id="test_session"
    )
    
    # Context should be limited
    assert len(chat_service.contexts["test_session"]) <= chat_service.max_context_messages + 2


def test_clear_context(chat_service):
    """Test clearing session context"""
    # Add some context
    chat_service.contexts["test_session"] = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"}
    ]
    
    # Clear context
    chat_service.clear_context("test_session")
    
    assert chat_service.contexts["test_session"] == []


def test_clear_nonexistent_context(chat_service):
    """Test clearing context that doesn't exist"""
    # Should not raise error
    chat_service.clear_context("nonexistent_session")


def test_get_context(chat_service):
    """Test getting session context"""
    # Add some context
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"}
    ]
    chat_service.contexts["test_session"] = messages
    
    # Get context
    context = chat_service.get_context("test_session")
    
    assert context == messages


def test_get_nonexistent_context(chat_service):
    """Test getting context that doesn't exist"""
    context = chat_service.get_context("nonexistent_session")
    assert context == []


@pytest.mark.asyncio
@patch("openai.OpenAI")
async def test_generate_response_api_error(mock_openai, chat_service):
    """Test error handling for OpenAI API errors"""
    import openai
    
    # Mock API error
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = openai.APIError("API Error")
    chat_service.client = mock_client
    
    # Should raise exception
    with pytest.raises(Exception) as exc_info:
        await chat_service.generate_response(
            message="Test",
            session_id="test_session"
        )
    
    assert "OpenAI API error" in str(exc_info.value)

