# Setup Guide - AI Chat Assistant

Step-by-step guide to set up and run the AI Chat Assistant application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting OpenAI API Key](#getting-openai-api-key)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Application](#running-the-application)
6. [Verification](#verification)
7. [Common Issues](#common-issues)

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Windows: Download from [python.org](https://www.python.org/downloads/)
   - macOS: `brew install python3`
   - Linux: `sudo apt-get install python3 python3-pip`

2. **Node.js 14 or higher**
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

3. **Git** (optional)
   - Download from [git-scm.com](https://git-scm.com/)

### Check Your Installation

```bash
# Check Python
python --version  # or python3 --version

# Check Node.js
node --version

# Check npm
npm --version

# Check pip
pip --version  # or pip3 --version
```

## Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (you won't be able to see it again!)
6. Save it securely

**Note:** OpenAI API usage is not free. Check [pricing](https://openai.com/pricing) and set up billing.

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- OpenAI
- SQLAlchemy
- Pytest
- And other dependencies

### Step 4: Create Environment File

**Windows:**
```bash
copy env.example .env
```

**macOS/Linux:**
```bash
cp env.example .env
```

### Step 5: Configure Environment Variables

Open `.env` in a text editor and update:

```env
# REQUIRED: Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Customize these if needed
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./chat_history.db
MAX_CONTEXT_MESSAGES=10
```

**Important:** Replace `sk-your-actual-api-key-here` with your real OpenAI API key!

### Step 6: Verify Backend Setup

Test that everything is installed correctly:

```bash
python -c "import fastapi, openai, sqlalchemy; print('All imports successful!')"
```

If you see "All imports successful!", you're ready to go!

## Frontend Setup

### Step 1: Navigate to Frontend Directory

Open a **new terminal** window:

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This may take a few minutes. It will install:
- React
- Axios
- Testing libraries
- And other dependencies

### Step 3: Create Environment File

**Windows:**
```bash
copy env.example .env
```

**macOS/Linux:**
```bash
cp env.example .env
```

### Step 4: Configure Environment Variables (Optional)

Open `.env` and verify/update:

```env
REACT_APP_API_URL=http://localhost:8000
```

Only change this if you're running the backend on a different port or domain.

### Step 5: Verify Frontend Setup

```bash
npm run build
```

If the build completes successfully, your frontend is ready!

## Running the Application

### Step 1: Start the Backend

In your backend terminal (with venv activated):

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Keep this terminal open!

### Step 2: Start the Frontend

In your frontend terminal:

```bash
cd frontend
npm start
```

You should see:
```
Compiled successfully!

You can now view chat-assistant-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

A browser window should open automatically to `http://localhost:3000`

## Verification

### 1. Check Backend is Running

Open a new terminal and run:

```bash
curl http://localhost:8000/api/health
```

You should see:
```json
{"status":"healthy","timestamp":"..."}
```

Or visit `http://localhost:8000/docs` in your browser to see the API documentation.

### 2. Check Frontend is Running

Open `http://localhost:3000` in your browser. You should see:
- AI Chat Assistant interface
- Welcome message
- Input box at the bottom
- Clear visual design

### 3. Test the Chat

1. Type a message like "Hello!"
2. Press Enter or click Send
3. Wait a few seconds
4. You should see the AI's response

**First message may take 5-10 seconds** as it connects to OpenAI.

### 4. Check Database

After sending a few messages:

```bash
# In backend directory
ls -la *.db
```

You should see `chat_history.db` file created.

## Common Issues

### Issue 1: "python: command not found"

**Solution:** Use `python3` instead:
```bash
python3 -m venv venv
python3 main.py
```

### Issue 2: "pip: command not found"

**Solution:** Use `pip3` or `python -m pip`:
```bash
python -m pip install -r requirements.txt
```

### Issue 3: "Cannot activate virtual environment"

**Windows PowerShell:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Windows CMD:**
```bash
venv\Scripts\activate.bat
```

### Issue 4: "Port 8000 already in use"

**Solution:** Kill the process or use a different port:

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or use a different port in backend `.env`:
```env
PORT=8001
```

### Issue 5: "Port 3000 already in use"

**Solution:** Use a different port:
```bash
PORT=3001 npm start
```

### Issue 6: "OpenAI API Error"

**Check:**
1. API key is correct (starts with `sk-`)
2. No extra spaces in `.env` file
3. API key has billing set up
4. You have remaining credits

**Test API key:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Issue 7: "Module not found" errors

**Backend:**
```bash
# Ensure venv is activated
# Then reinstall
pip install -r requirements.txt
```

**Frontend:**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue 8: Cannot connect to backend from frontend

**Check:**
1. Backend is running (check terminal)
2. Backend URL is correct in frontend `.env`
3. No firewall blocking
4. Check browser console for CORS errors

### Issue 9: Database permission errors

**Solution:** Check write permissions:

**Windows:**
```bash
icacls chat_history.db
```

**macOS/Linux:**
```bash
chmod 666 chat_history.db
```

## Quick Troubleshooting Commands

```bash
# Backend health check
curl http://localhost:8000/api/health

# Check Python installation
python --version

# Check Node installation
node --version

# Check if ports are in use
netstat -an | grep 8000  # Backend
netstat -an | grep 3000  # Frontend

# View backend logs
# (check terminal where you ran python main.py)

# View frontend logs
# (check terminal where you ran npm start)
```

## Getting Help

If you're still having issues:

1. **Check the logs** in both terminals
2. **Read error messages** carefully
3. **Search the error** on Google/Stack Overflow
4. **Check OpenAI status**: https://status.openai.com/
5. **Review the README.md** for more details

## Next Steps

Once everything is running:

1. **Explore the chat interface** - Try different types of questions
2. **Check the API documentation** - Visit http://localhost:8000/docs
3. **Run the tests** - See TEST_GUIDE.md
4. **Read the API docs** - See API_DOCUMENTATION.md
5. **Customize the assistant** - Modify the system prompt in `chat_service.py`

## Quick Start Script

Save this as `start.sh` (macOS/Linux) or `start.bat` (Windows):

**start.sh:**
```bash
#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
cd ../frontend
npm start

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
```

**start.bat:**
```batch
@echo off

:: Start backend
cd backend
call venv\Scripts\activate
start "Backend" python main.py

:: Wait for backend
timeout /t 5

:: Start frontend
cd ..\frontend
npm start
```

Make executable (macOS/Linux):
```bash
chmod +x start.sh
./start.sh
```

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] OpenAI API key obtained
- [ ] Backend dependencies installed
- [ ] Backend `.env` configured
- [ ] Frontend dependencies installed
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:3000
- [ ] Can send messages and get responses
- [ ] Database file created

Congratulations! You're all set up! 🎉

