# AI Chat Assistant - Frontend

React-based frontend for the AI Chat Assistant application.

## Overview

A modern, responsive chat interface that provides:
- Real-time messaging
- Typing indicators
- Chat history
- Session management
- Mobile-friendly design

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Set up environment:
```bash
cp env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

3. Start development server:
```bash
npm start
```

## Available Scripts

- `npm start` - Run development server
- `npm test` - Run tests
- `npm run build` - Build for production
- `npm run eject` - Eject from Create React App (irreversible)

## Project Structure

```
src/
├── components/
│   ├── ChatMessage.js       # Message display component
│   ├── TypingIndicator.js   # Typing animation
│   └── *.test.js           # Component tests
├── services/
│   └── chatService.js      # API client
├── App.js                  # Main application
└── index.js               # Entry point
```

## Testing

Run tests:
```bash
npm test
```

With coverage:
```bash
npm test -- --coverage
```

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

