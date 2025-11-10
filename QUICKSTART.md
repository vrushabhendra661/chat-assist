# Quick Start Guide

Get the AI Chat Assistant running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 14+ installed
- OpenAI API key

## Step 1: Get OpenAI API Key (2 minutes)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Visit https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

## Step 2: Setup Backend (2 minutes)

Open a terminal in the project directory:

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Windows:
copy env.example .env
# Mac/Linux:
cp env.example .env
```

**Edit `.env` file and paste your OpenAI API key:**
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Setup Frontend (1 minute)

Open a **NEW** terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file (optional)
# Windows:
copy env.example .env
# Mac/Linux:
cp env.example .env
```

## Step 4: Run the Application

**Terminal 1 (Backend):**
```bash
cd backend
# Activate venv if not already
python main.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

Browser should open automatically to `http://localhost:3000`

## Step 5: Test It!

1. Type "Hello!" in the chat
2. Press Enter or click Send
3. Wait a few seconds
4. See the AI response!

## Troubleshooting

### "python: command not found"
Try `python3` instead of `python`

### "pip: command not found"
Try `python -m pip` instead of `pip`

### Backend won't start
- Check that port 8000 is free
- Verify your OpenAI API key is correct
- Ensure virtual environment is activated

### Frontend won't start
- Check that port 3000 is free
- Try deleting `node_modules` and running `npm install` again
- Clear browser cache

### Can't connect to backend
- Ensure backend is running (check Terminal 1)
- Verify backend URL in frontend `.env` is correct
- Check browser console for errors

### OpenAI API error
- Verify API key is correct (no extra spaces)
- Check you have billing set up on OpenAI
- Ensure you have remaining credits

## Need More Help?

- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- See [README.md](README.md) for complete documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details

## What's Next?

Once running, try:
- Asking different types of questions
- Starting a new conversation
- Clearing the chat
- Testing on mobile (visit from phone on same network)

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

## Stopping the Application

Press `Ctrl+C` in both terminal windows.

---

**Enjoy your AI Chat Assistant!** 🎉

