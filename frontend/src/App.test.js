import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import chatService from './services/chatService';

// Mock the chat service
jest.mock('./services/chatService');

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    chatService.getHistory.mockResolvedValue([]);
  });

  test('renders chat interface', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
    });
    
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
  });

  test('displays welcome message when no messages', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Welcome to AI Chat Assistant!')).toBeInTheDocument();
    });
  });

  test('sends message and displays response', async () => {
    chatService.sendMessage.mockResolvedValue({
      response: 'Hello! How can I help you?',
      session_id: 'test_session',
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByTitle('Send message');

    // Type a message
    fireEvent.change(input, { target: { value: 'Hello' } });
    expect(input.value).toBe('Hello');

    // Send the message
    fireEvent.click(sendButton);

    // Wait for the response
    await waitFor(() => {
      expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });
  });

  test('clears input after sending message', async () => {
    chatService.sendMessage.mockResolvedValue({
      response: 'Response',
      session_id: 'test_session',
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.submit(input.closest('form'));

    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });

  test('displays error message on API failure', async () => {
    chatService.sendMessage.mockRejectedValue(new Error('API Error'));

    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.submit(input.closest('form'));

    await waitFor(() => {
      expect(screen.getByText('Failed to get response. Please try again.')).toBeInTheDocument();
    });
  });

  test('prevents sending empty messages', () => {
    render(<App />);
    
    const sendButton = screen.getByTitle('Send message');
    
    expect(sendButton).toBeDisabled();
  });

  test('clears chat when clear button is clicked', async () => {
    // Mock window.confirm
    window.confirm = jest.fn(() => true);
    chatService.clearSession.mockResolvedValue({ message: 'Session cleared' });

    // Add a message first
    chatService.sendMessage.mockResolvedValue({
      response: 'Test response',
      session_id: 'test_session',
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.submit(input.closest('form'));

    await waitFor(() => {
      expect(screen.getByText('Test response')).toBeInTheDocument();
    });

    // Click clear button
    const clearButton = screen.getByTitle('Clear Chat');
    fireEvent.click(clearButton);

    await waitFor(() => {
      expect(screen.queryByText('Test response')).not.toBeInTheDocument();
    });
  });

  test('fills input with suggestion when suggestion is clicked', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('What can you help me with?')).toBeInTheDocument();
    });

    const suggestion = screen.getByText('What can you help me with?');
    fireEvent.click(suggestion);

    const input = screen.getByPlaceholderText('Type your message here...');
    expect(input.value).toBe('What can you help me with?');
  });
});

