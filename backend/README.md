# AI Chat Assistant - Backend

FastAPI-based backend service for the AI Chat Assistant application.

## Overview

This backend provides RESTful API endpoints for:
- Processing chat messages with OpenAI GPT
- Managing conversation context
- Storing and retrieving chat history
- Session management

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Run the server:
```bash
python main.py
```

## API Endpoints

- `POST /api/chat` - Send a message and get AI response
- `POST /api/clear` - Clear session context
- `GET /api/history/{session_id}` - Get chat history
- `GET /api/health` - Health check

## Testing

Run tests with:
```bash
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

## Architecture

- `main.py` - FastAPI application and route handlers
- `chat_service.py` - Business logic for AI interactions
- `database.py` - SQLAlchemy models and database setup

## Environment Variables

See `env.example` for required configuration.

