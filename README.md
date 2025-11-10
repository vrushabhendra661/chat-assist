# AI Chat Assistant

An intelligent, AI-powered chat assistant built with React and FastAPI that provides context-aware conversational responses using OpenAI's GPT models.

![AI Chat Assistant](https://img.shields.io/badge/AI-Chat%20Assistant-blue)
![React](https://img.shields.io/badge/React-18.2.0-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This AI Chat Assistant is a full-stack application that demonstrates modern web development practices and AI integration. It features:

- **Intelligent Conversations**: Powered by OpenAI's GPT-3.5-turbo model for natural language understanding and generation
- **Context Management**: Maintains conversation history within sessions for contextually relevant responses
- **Persistent Storage**: SQLite database for chat history analytics and personalization
- **Modern UI/UX**: Beautiful, responsive interface with smooth animations and mobile support
- **Production-Ready**: Comprehensive error handling, logging, and testing

## ✨ Features

### Frontend Features
- 💬 Clean, intuitive chat interface
- 📱 Fully responsive design (desktop and mobile)
- ⚡ Real-time message updates
- 🎨 Visual distinction between user and assistant messages
- ⌨️ Typing indicator during AI response generation
- 🗑️ Clear conversation and start new session options
- 🎯 Quick suggestion buttons for common queries
- ⏱️ Message timestamps
- 🌈 Modern gradient design with smooth animations

### Backend Features
- 🤖 OpenAI GPT-3.5-turbo integration
- 💾 Context-aware conversation management
- 🗄️ SQLite database for persistent chat history
- 🔒 Session-based isolation
- 📝 Comprehensive logging
- 🛡️ Error handling and validation
- 🔌 RESTful API with CORS support
- 📊 Health check endpoint

## 🏗️ Architecture

```
┌─────────────┐      HTTP/JSON      ┌─────────────┐      OpenAI API      ┌─────────────┐
│   React     │◄──────────────────►│   FastAPI   │◄───────────────────►│   OpenAI    │
│  Frontend   │                     │   Backend   │                      │     GPT     │
└─────────────┘                     └─────────────┘                      └─────────────┘
                                            │
                                            │ SQLAlchemy
                                            ▼
                                    ┌─────────────┐
                                    │   SQLite    │
                                    │  Database   │
                                    └─────────────┘
```

### Components:
1. **Frontend (React)**: User interface with chat components
2. **Backend (FastAPI)**: REST API server handling requests
3. **Chat Service**: Business logic for AI interactions
4. **Database**: Persistent storage for chat history
5. **OpenAI API**: AI model for response generation

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** and npm - [Download](https://nodejs.org/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
- **Git** (optional) - [Download](https://git-scm.com/)

## 🚀 Installation

### Clone the Repository

```bash
git clone <repository-url>
cd chat-bot
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

4. (Optional) Update API URL in `.env` if needed:
```env
REACT_APP_API_URL=http://localhost:8000
```

## ⚙️ Configuration

### Backend Configuration

Edit `backend/.env` to configure:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///./chat_history.db

# Application Settings
MAX_CONTEXT_MESSAGES=10  # Maximum messages to keep in context
```

### Frontend Configuration

Edit `frontend/.env` to configure:

```env
REACT_APP_API_URL=http://localhost:8000  # Backend API URL
```

## 🏃 Running the Application

### Start the Backend

1. Open a terminal and navigate to the backend directory:
```bash
cd backend
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Start the Frontend

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Start the React development server:
```bash
npm start
```

The application will open automatically at: `http://localhost:3000`

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Root Endpoint
```http
GET /
```

**Response:**
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

#### 2. Chat Endpoint
```http
POST /api/chat
```

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "session_123"  // Optional, defaults to "default"
}
```

**Response:**
```json
{
  "response": "I'm doing great! How can I help you today?",
  "session_id": "session_123"
}
```

**Error Response:**
```json
{
  "detail": "Failed to generate response: error message"
}
```

#### 3. Clear Session
```http
POST /api/clear
```

**Request Body:**
```json
{
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "message": "Session session_123 cleared successfully"
}
```

#### 4. Get Chat History
```http
GET /api/history/{session_id}?limit=50
```

**Parameters:**
- `session_id` (path): Session identifier
- `limit` (query): Maximum number of messages (default: 50)

**Response:**
```json
[
  {
    "id": 1,
    "user_message": "Hello",
    "assistant_response": "Hi! How can I help?",
    "timestamp": "2024-01-01T12:00:00",
    "session_id": "session_123"
  }
]
```

#### 5. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

### Backend Tests

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest test_api.py
pytest test_chat_service.py
```

### Frontend Tests

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Run tests:
```bash
npm test
```

Run with coverage:
```bash
npm test -- --coverage
```

Run in watch mode:
```bash
npm test -- --watch
```

### Test Coverage

The project includes comprehensive tests for:

**Backend:**
- ✅ API endpoint functionality
- ✅ Chat service logic
- ✅ Context management
- ✅ Error handling
- ✅ Database operations

**Frontend:**
- ✅ Component rendering
- ✅ User interactions
- ✅ API integration
- ✅ State management
- ✅ Error handling

## 📁 Project Structure

```
chat-bot/
├── backend/
│   ├── main.py                 # FastAPI application and endpoints
│   ├── chat_service.py         # Chat logic and OpenAI integration
│   ├── database.py             # Database models and configuration
│   ├── requirements.txt        # Python dependencies
│   ├── env.example             # Environment variables template
│   ├── pytest.ini              # Pytest configuration
│   ├── test_api.py             # API endpoint tests
│   └── test_chat_service.py    # Chat service tests
│
├── frontend/
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatMessage.js       # Message component
│   │   │   ├── ChatMessage.css
│   │   │   ├── ChatMessage.test.js
│   │   │   ├── TypingIndicator.js   # Typing animation
│   │   │   ├── TypingIndicator.css
│   │   │   └── TypingIndicator.test.js
│   │   ├── services/
│   │   │   └── chatService.js       # API client
│   │   ├── App.js              # Main application component
│   │   ├── App.css             # Main styles
│   │   ├── App.test.js         # App tests
│   │   ├── index.js            # Entry point
│   │   ├── index.css           # Global styles
│   │   └── setupTests.js       # Test configuration
│   ├── package.json            # Node dependencies
│   └── env.example             # Environment variables template
│
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🛠️ Technologies Used

### Frontend
- **React 18.2.0** - UI library
- **Axios** - HTTP client
- **CSS3** - Styling with modern features
- **React Testing Library** - Component testing
- **Jest** - Test framework

### Backend
- **FastAPI 0.104.1** - Modern Python web framework
- **Python 3.8+** - Programming language
- **OpenAI API 1.3.5** - GPT model integration
- **SQLAlchemy 2.0.23** - ORM for database
- **SQLite** - Lightweight database
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server

### AI/ML
- **OpenAI GPT-3.5-turbo** - Language model
- **Natural Language Processing** - Context understanding

## 🌐 Deployment

### Backend Deployment

#### Using Uvicorn (Production)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deployment Platforms
- **Heroku**: Use Procfile
- **AWS**: EC2, Elastic Beanstalk, or Lambda
- **Google Cloud**: App Engine or Cloud Run
- **DigitalOcean**: App Platform

### Frontend Deployment

#### Build for Production
```bash
npm run build
```

#### Deployment Platforms
- **Netlify**: Automatic deployment from Git
- **Vercel**: Optimized for React apps
- **AWS S3 + CloudFront**: Static hosting
- **GitHub Pages**: Free hosting

### Environment Variables in Production

Ensure these are set in your production environment:

**Backend:**
```env
OPENAI_API_KEY=your_production_key
DATABASE_URL=your_production_db_url
```

**Frontend:**
```env
REACT_APP_API_URL=https://your-api-domain.com
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues

**1. Module not found errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**2. OpenAI API errors**
- Verify API key is correct in `.env`
- Check API usage limits on OpenAI dashboard
- Ensure API key has proper permissions

**3. Database errors**
- Delete `chat_history.db` and restart (will lose data)
- Check write permissions in backend directory

**4. CORS errors**
- Verify frontend URL is in CORS allowed origins
- Check backend is running on correct port

#### Frontend Issues

**1. Cannot connect to backend**
- Ensure backend is running
- Verify `REACT_APP_API_URL` in `.env`
- Check browser console for errors

**2. Build errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**3. Port already in use**
```bash
# Use different port
PORT=3001 npm start
```

### Debug Mode

Enable debug logging in backend by modifying `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If you encounter issues:
1. Check the error messages in console/logs
2. Review the API documentation
3. Check OpenAI API status
4. Review this README's troubleshooting section

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint rules for JavaScript
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

---

