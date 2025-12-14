import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event'; // Import user-event
import { axe, toHaveNoViolations } from 'jest-axe';
import { ChatWindow } from '@/components/ChatWindow';
import { useChat } from '@/hooks/use-chat';

expect.extend(toHaveNoViolations);

// Mock the useChat hook
jest.mock('@/hooks/use-chat', () => ({
  useChat: jest.fn(),
}));

describe('ChatWindow Accessibility', () => {
  beforeEach(() => {
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      sendMessage: jest.fn(),
      isLoading: false,
    });
  });

  it('should have no accessibility violations', async () => {
    const { container } = render(<ChatWindow userRole="user" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should allow keyboard navigation to input and send button', async () => {
    const user = userEvent.setup(); // Setup user-event
    render(<ChatWindow userRole="user" />);

    const input = screen.getByPlaceholderText('Type your question...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    await user.tab(); // Tab to the input
    expect(input).toHaveFocus();

    // Type something to enable the send button
    await user.type(input, 'test'); 

    await user.tab(); // Tab to the send button
    expect(sendButton).toHaveFocus();
  });

  // Test submitting with Enter key
  it('should submit message on Enter key press in input field', async () => {
    const user = userEvent.setup();
    const sendMessageMock = jest.fn();
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      sendMessage: sendMessageMock,
      isLoading: false,
    });

    render(<ChatWindow userRole="user" />);
    const input = screen.getByPlaceholderText('Type your question...');
    
    await user.type(input, 'Test message'); // Type into input
    await user.keyboard('{enter}'); // Simulate Enter key press

    expect(sendMessageMock).toHaveBeenCalledWith('Test message');
    expect(input).toHaveValue(''); // Input should be cleared
  });
});
