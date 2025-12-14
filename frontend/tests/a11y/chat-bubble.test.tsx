import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { ChatBubble, ChatBubbleProps } from '@/components/ChatBubble';

expect.extend(toHaveNoViolations);

describe('ChatBubble Accessibility', () => {
  const defaultProps: ChatBubbleProps = {
    role: 'assistant',
    content: 'Hello, how can I help you?',
    messageId: 'msg-123',
    chatSessionId: 'sess-456',
  };

  it('should have no accessibility violations for assistant message', async () => {
    const { container } = render(<ChatBubble {...defaultProps} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no accessibility violations for user message', async () => {
    const { container } = render(<ChatBubble {...defaultProps} role="user" content="My question" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no accessibility violations with citations', async () => {
    const propsWithCitations: ChatBubbleProps = {
      ...defaultProps,
      citations: [
        { title: 'Doc 1', url: 'http://example.com/doc1' },
        { title: 'Doc 2', url: 'http://example.com/doc2' },
      ],
    };
    const { container } = render(<ChatBubble {...propsWithCitations} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no accessibility violations with suggested queries', async () => {
    const onSuggestionClickMock = jest.fn();
    const propsWithSuggestions: ChatBubbleProps = {
      ...defaultProps,
      suggestedQueries: ['Query 1', 'Query 2'],
      onSuggestionClick: onSuggestionClickMock,
    };
    const { container } = render(<ChatBubble {...propsWithSuggestions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();

    // Verify suggested query buttons are clickable and trigger handler
    fireEvent.click(screen.getByRole('button', { name: 'Query 1' }));
    expect(onSuggestionClickMock).toHaveBeenCalledWith('Query 1');
  });
});
