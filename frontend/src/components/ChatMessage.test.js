import { render, screen } from '@testing-library/react';
import ChatMessage from './ChatMessage';

describe('ChatMessage Component', () => {
  const mockTimestamp = new Date('2024-01-01T12:00:00').toISOString();

  test('renders user message correctly', () => {
    render(
      <ChatMessage 
        message="Hello, this is a user message" 
        sender="user" 
        timestamp={mockTimestamp}
      />
    );

    expect(screen.getByText('Hello, this is a user message')).toBeInTheDocument();
    const wrapper = screen.getByText('Hello, this is a user message').closest('.message-wrapper');
    expect(wrapper).toHaveClass('user');
  });

  test('renders assistant message correctly', () => {
    render(
      <ChatMessage 
        message="Hello, this is an assistant message" 
        sender="assistant" 
        timestamp={mockTimestamp}
      />
    );

    expect(screen.getByText('Hello, this is an assistant message')).toBeInTheDocument();
    const wrapper = screen.getByText('Hello, this is an assistant message').closest('.message-wrapper');
    expect(wrapper).toHaveClass('assistant');
  });

  test('displays formatted timestamp', () => {
    render(
      <ChatMessage 
        message="Test message" 
        sender="user" 
        timestamp={mockTimestamp}
      />
    );

    // Check if timestamp is displayed (format may vary by locale)
    const timestamp = screen.getByText(/\d{1,2}:\d{2}/);
    expect(timestamp).toBeInTheDocument();
  });

  test('renders avatar for user message', () => {
    const { container } = render(
      <ChatMessage 
        message="Test" 
        sender="user" 
        timestamp={mockTimestamp}
      />
    );

    const avatar = container.querySelector('.message-avatar');
    expect(avatar).toBeInTheDocument();
  });

  test('renders avatar for assistant message', () => {
    const { container } = render(
      <ChatMessage 
        message="Test" 
        sender="assistant" 
        timestamp={mockTimestamp}
      />
    );

    const avatar = container.querySelector('.message-avatar');
    expect(avatar).toBeInTheDocument();
  });
});

