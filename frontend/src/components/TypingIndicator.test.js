import { render } from '@testing-library/react';
import TypingIndicator from './TypingIndicator';

describe('TypingIndicator Component', () => {
  test('renders typing indicator', () => {
    const { container } = render(<TypingIndicator />);
    
    const typingIndicator = container.querySelector('.typing-indicator');
    expect(typingIndicator).toBeInTheDocument();
  });

  test('renders three dots', () => {
    const { container } = render(<TypingIndicator />);
    
    const dots = container.querySelectorAll('.typing-indicator span');
    expect(dots.length).toBe(3);
  });

  test('has assistant styling', () => {
    const { container } = render(<TypingIndicator />);
    
    const wrapper = container.querySelector('.message-wrapper');
    expect(wrapper).toHaveClass('assistant');
  });

  test('renders avatar', () => {
    const { container } = render(<TypingIndicator />);
    
    const avatar = container.querySelector('.message-avatar');
    expect(avatar).toBeInTheDocument();
  });
});

