import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatBubble } from '@/components/ChatBubble';

// Mock the FeedbackButtons component
jest.mock('@/components/FeedbackButtons', () => ({
  FeedbackButtons: jest.fn(({ messageId, chatSessionId }) => (
    <div data-testid="mock-feedback-buttons" data-message-id={messageId} data-chat-session-id={chatSessionId}>
      Mock Feedback Buttons
    </div>
  )),
}));

describe('ChatBubble', () => {
  const defaultMessageId = "msg-123";
  const defaultChatSessionId = "session-456";

  it('renders user message with primary background and no feedback buttons', () => {
    render(<ChatBubble role="user" content="Hello bot" messageId={defaultMessageId} chatSessionId={defaultChatSessionId} />);
    const message = screen.getByText('Hello bot');
    expect(message).toBeInTheDocument();
    expect(message.closest('.flex')).toHaveClass('justify-end');
    expect(screen.queryByTestId('mock-feedback-buttons')).not.toBeInTheDocument();
  });

  it('renders assistant message with muted background and feedback buttons', () => {
    render(<ChatBubble role="assistant" content="Hello user" messageId={defaultMessageId} chatSessionId={defaultChatSessionId} />);
    const message = screen.getByText('Hello user');
    expect(message).toBeInTheDocument();
    expect(message.closest('.flex')).toHaveClass('justify-start');
    
    const feedbackButtons = screen.getByTestId('mock-feedback-buttons');
    expect(feedbackButtons).toBeInTheDocument();
    expect(feedbackButtons).toHaveAttribute('data-message-id', defaultMessageId);
    expect(feedbackButtons).toHaveAttribute('data-chat-session-id', defaultChatSessionId);
  });

  it('renders content', () => {
    render(<ChatBubble role="assistant" content="**Bold** text" messageId={defaultMessageId} chatSessionId={defaultChatSessionId} />);
    expect(screen.getByText('**Bold** text')).toBeInTheDocument();
  });

  it('renders citations when provided', () => {
    const citations = [{ title: 'Source 1', url: 'http://source1.com' }];
    render(<ChatBubble role="assistant" content="Answer" citations={citations} messageId={defaultMessageId} chatSessionId={defaultChatSessionId} />);

    expect(screen.getByText('Source:')).toBeInTheDocument();

    const link = screen.getByRole('link', { name: 'Source 1' });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'http://source1.com');
  });

  it('renders typing indicator when isStreaming is true', () => {
    render(<ChatBubble role="assistant" content="Typing" messageId={defaultMessageId} chatSessionId={defaultChatSessionId} isStreaming={true} />);

    const typingIndicators = screen.getAllByText('.');
    expect(typingIndicators.length).toBeGreaterThanOrEqual(3);
  });

  it('does not render typing indicator when isStreaming is false', () => {
    const { container } = render(<ChatBubble role="assistant" content="Done" messageId={defaultMessageId} chatSessionId={defaultChatSessionId} isStreaming={false} />);

    const typingIndicator = container.querySelector('.animate-bounce');
    expect(typingIndicator).not.toBeInTheDocument();
  });
});