import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatBubble } from '@/components/ChatBubble';

describe('ChatBubble', () => {
  it('renders user message with primary background', () => {
    render(<ChatBubble role="user" content="Hello bot" />);
    const message = screen.getByText('Hello bot');
    expect(message).toBeInTheDocument();
    // Check for parent div having justify-end
    expect(message.closest('.flex')).toHaveClass('justify-end');
  });

  it('renders assistant message with muted background', () => {
    render(<ChatBubble role="assistant" content="Hello user" />);
    const message = screen.getByText('Hello user');
    expect(message).toBeInTheDocument();
    // Check for parent div having justify-start
    expect(message.closest('.flex')).toHaveClass('justify-start');
  });

  it('renders content', () => {
    render(<ChatBubble role="assistant" content="**Bold** text" />);
    // Since we mock ReactMarkdown, it just renders the text
    expect(screen.getByText('**Bold** text')).toBeInTheDocument();
  });

  it('renders citations when provided', () => {
    const citations = [{ title: 'Source 1', url: 'http://source1.com' }];
    render(<ChatBubble role="assistant" content="Answer" citations={citations} />);
    
    expect(screen.getByText('Source:')).toBeInTheDocument();
    
    const link = screen.getByRole('link', { name: 'Source 1' });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'http://source1.com');
  });
});