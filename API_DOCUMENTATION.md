# API Documentation

Complete API reference for the AI Chat Assistant backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing:
- API keys
- JWT tokens
- OAuth 2.0

## Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:** `200 OK`

```json
{
  "message": "AI Chat Assistant API",
  "version": "1.0.0",
  "endpoints": {
    "chat": "/api/chat",
    "clear": "/api/clear",
    "history": "/api/history/{session_id}",
    "health": "/api/health"
  }
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### 2. Chat Endpoint

Send a message and receive an AI-generated response.

**Endpoint:** `POST /api/chat`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | User's message to the AI |
| session_id | string | No | Session identifier (default: "default") |

**Request Example:**
```json
{
  "message": "What is machine learning?",
  "session_id": "session_abc123"
}
```

**Response:** `200 OK`

```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "session_id": "session_abc123"
}
```

**Error Response:** `500 Internal Server Error`

```json
{
  "detail": "Failed to generate response: error message"
}
```

**Error Response:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test_session"}'
```

**Notes:**
- The AI maintains context within the same session
- Context is limited to the last 10 messages (configurable)
- Long responses may be truncated (max 500 tokens)

---

### 3. Clear Session

Clear conversation context for a specific session.

**Endpoint:** `POST /api/clear`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| session_id | string | Yes | Session identifier to clear |

**Request Example:**
```json
{
  "session_id": "session_abc123"
}
```

**Response:** `200 OK`

```json
{
  "message": "Session session_abc123 cleared successfully"
}
```

**Error Response:** `500 Internal Server Error`

```json
{
  "detail": "Failed to clear session: error message"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/clear \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test_session"}'
```

**Notes:**
- Clears in-memory context only (not database history)
- Does not affect other sessions
- Safe to call even if session doesn't exist

---

### 4. Get Chat History

Retrieve chat history for a specific session.

**Endpoint:** `GET /api/history/{session_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 50 | Maximum number of messages |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "user_message": "Hello!",
    "assistant_response": "Hi! How can I help you?",
    "timestamp": "2024-01-01T12:00:00",
    "session_id": "session_abc123"
  },
  {
    "id": 2,
    "user_message": "What is AI?",
    "assistant_response": "AI stands for Artificial Intelligence...",
    "timestamp": "2024-01-01T12:01:00",
    "session_id": "session_abc123"
  }
]
```

**Error Response:** `500 Internal Server Error`

```json
{
  "detail": "Failed to retrieve history: error message"
}
```

**Example:**
```bash
curl http://localhost:8000/api/history/test_session?limit=20
```

**Notes:**
- Returns messages in chronological order (oldest first)
- Empty array if no history exists
- Timestamps are in UTC ISO format

---

### 5. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Example:**
```bash
curl http://localhost:8000/api/health
```

**Notes:**
- Used for monitoring and load balancer checks
- Always returns 200 if server is running
- Timestamp is in UTC ISO format

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 422 | Validation error (invalid request) |
| 500 | Internal server error |

## Rate Limiting

Currently not implemented. For production, consider:
- Rate limiting per session/IP
- Request throttling
- Cost management for OpenAI API

## Error Handling

All errors follow FastAPI's standard format:

```json
{
  "detail": "Error message description"
}
```

Validation errors include field-specific information:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Test endpoints directly
- View request/response schemas
- See detailed documentation
- Try API calls interactively

## Request/Response Examples

### Example 1: Basic Chat Conversation

```bash
# Send first message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "conv_1"}'

# Response
{
  "response": "Hello! How can I assist you today?",
  "session_id": "conv_1"
}

# Send follow-up (maintains context)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What did I just say?", "session_id": "conv_1"}'

# Response
{
  "response": "You said 'Hello!' to greet me.",
  "session_id": "conv_1"
}
```

### Example 2: Get History

```bash
curl http://localhost:8000/api/history/conv_1

# Response
[
  {
    "id": 1,
    "user_message": "Hello!",
    "assistant_response": "Hello! How can I assist you today?",
    "timestamp": "2024-01-01T12:00:00",
    "session_id": "conv_1"
  },
  {
    "id": 2,
    "user_message": "What did I just say?",
    "assistant_response": "You said 'Hello!' to greet me.",
    "timestamp": "2024-01-01T12:00:30",
    "session_id": "conv_1"
  }
]
```

### Example 3: Clear and Start New

```bash
# Clear session
curl -X POST http://localhost:8000/api/clear \
  -H "Content-Type: application/json" \
  -d '{"session_id": "conv_1"}'

# Start fresh conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What did I say before?", "session_id": "conv_1"}'

# Response (no context from before)
{
  "response": "I don't have any information about what you said before...",
  "session_id": "conv_1"
}
```

## Best Practices

1. **Session Management**
   - Use unique session IDs for different conversations
   - Clear sessions when starting new conversations
   - Implement session expiration in production

2. **Error Handling**
   - Always check response status codes
   - Handle network errors gracefully
   - Retry failed requests with exponential backoff

3. **Performance**
   - Limit context size for faster responses
   - Use pagination for history retrieval
   - Implement caching where appropriate

4. **Security**
   - Use HTTPS in production
   - Implement authentication
   - Validate and sanitize all inputs
   - Rate limit requests

## Troubleshooting

### Common Issues

**1. Connection Refused**
- Ensure backend is running
- Check port 8000 is not in use
- Verify firewall settings

**2. 500 Internal Server Error**
- Check OpenAI API key is valid
- Verify API key has credits
- Check server logs for details

**3. 422 Validation Error**
- Verify request body format
- Check required fields are present
- Ensure field types are correct

### Debug Tips

Enable detailed logging in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

Check server logs for error details.

## Support

For issues or questions:
- Check interactive documentation at `/docs`
- Review error messages in response
- Enable debug logging
- Check OpenAI API status

