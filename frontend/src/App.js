import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import ChatMessage from './components/ChatMessage';
import TypingIndicator from './components/TypingIndicator';
import chatService from './services/chatService';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    // Load chat history on mount
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const history = await chatService.getHistory(sessionId);
      const formattedMessages = history.flatMap(item => [
        { text: item.user_message, sender: 'user', timestamp: item.timestamp },
        { text: item.assistant_response, sender: 'assistant', timestamp: item.timestamp }
      ]);
      setMessages(formattedMessages);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) {
      return;
    }

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setError(null);

    // Add user message to chat
    const newUserMessage = {
      text: userMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await chatService.sendMessage(userMessage, sessionId);
      
      // Add assistant response to chat
      const assistantMessage = {
        text: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      try {
        await chatService.clearSession(sessionId);
        setMessages([]);
        setError(null);
      } catch (err) {
        setError('Failed to clear chat. Please try again.');
        console.error('Error clearing chat:', err);
      }
    }
  };

  const handleNewSession = () => {
    if (window.confirm('Start a new session? Current chat will remain in history.')) {
      window.location.reload();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        {/* Header */}
        <div className="chat-header">
          <div className="header-content">
            <div className="header-title">
              <div className="bot-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
                  <circle cx="9" cy="14" r="1" />
                  <circle cx="15" cy="14" r="1" />
                  <path d="M9 17.5c0 .83.67 1.5 1.5 1.5h3c.83 0 1.5-.67 1.5-1.5" />
                </svg>
              </div>
              <div>
                <h1>AI Chat Assistant</h1>
                <p>Powered by OpenAI GPT</p>
              </div>
            </div>
            <div className="header-actions">
              <button 
                className="icon-button" 
                onClick={handleNewSession}
                title="New Session"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 5v14M5 12h14" />
                </svg>
              </button>
              <button 
                className="icon-button" 
                onClick={handleClearChat}
                title="Clear Chat"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.length === 0 && !isLoading && (
            <div className="welcome-message">
              <div className="welcome-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <h2>Welcome to AI Chat Assistant!</h2>
              <p>Start a conversation by typing a message below.</p>
              <div className="suggestions">
                <button onClick={() => setInputMessage("What can you help me with?")}>
                  What can you help me with?
                </button>
                <button onClick={() => setInputMessage("Tell me a fun fact")}>
                  Tell me a fun fact
                </button>
                <button onClick={() => setInputMessage("Explain quantum computing")}>
                  Explain quantum computing
                </button>
              </div>
            </div>
          )}
          
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message.text}
              sender={message.sender}
              timestamp={message.timestamp}
            />
          ))}
          
          {isLoading && <TypingIndicator />}
          
          {error && (
            <div className="error-message">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 8v4M12 16h.01" />
              </svg>
              <span>{error}</span>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="input-container">
          <form onSubmit={handleSendMessage} className="input-form">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message here..."
              disabled={isLoading}
              className="message-input"
            />
            <button 
              type="submit" 
              disabled={!inputMessage.trim() || isLoading}
              className="send-button"
              title="Send message"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;

