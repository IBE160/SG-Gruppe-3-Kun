import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatWindow } from '@/components/ChatWindow';
import { useChat } from '@/hooks/use-chat';
import { Message } from '@/hooks/use-chat';

// Mock scrollIntoView
window.HTMLElement.prototype.scrollIntoView = jest.fn();

// Mock the useChat hook
jest.mock('@/hooks/use-chat', () => ({
  useChat: jest.fn(),
}));

// Mock the ChatBubble component to inspect props
jest.mock('@/components/ChatBubble', () => ({
  ChatBubble: jest.fn(({ role, content, citations, messageId, chatSessionId }) => (
    <div data-testid="mock-chat-bubble" data-role={role} data-content={content} data-message-id={messageId} data-chat-session-id={chatSessionId}>
      {content}
      {citations && citations.length > 0 && (
        <div data-testid="mock-citations">Source: {citations[0].title}</div>
      )}
    </div>
  )),
}));


// Cast useChat to a Mock, so we can control its return values
const mockUseChat = useChat as jest.MockedFunction<typeof useChat>;

// Define variables to hold the current state of the mock hook
let mockMessages: Message[] = [];
let mockIsLoading: boolean = false;
let mockSendMessage: jest.Mock;


describe('ChatWindow', () => {
  let rerender: (ui: React.ReactElement) => void;

  beforeEach(() => {
    mockUseChat.mockReset(); // Reset the mock before each test

    mockMessages = [];
    mockIsLoading = false;
    
    mockSendMessage = jest.fn(async (content: string) => {
      const userMessageId = `user-${Date.now()}`;
      mockMessages = [...mockMessages, { id: userMessageId, role: 'user', content }];
      mockIsLoading = true;
      act(() => { rerender(<ChatWindow userRole="Project Manager / Admin" />); });
      
      await new Promise(resolve => setTimeout(resolve, 50)); 
      
      const assistantMessageId = `assistant-${Date.now() + 1}`;
      const botResponse: Message = { 
        id: assistantMessageId, 
        role: 'assistant', 
        content: 'This is a mock response about login.', 
        citations: [{ title: 'Login Guide', url: 'https://docs.example.com/login' }] 
      };
      mockMessages = [...mockMessages, botResponse];
      mockIsLoading = false;
      act(() => { rerender(<ChatWindow userRole="Project Manager / Admin" />); });
    });

    mockUseChat.mockImplementation(() => ({ // Removed userRole parameter
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: mockIsLoading,
    }));
  });

  it('renders initial empty state', () => {
    const renderResult = render(<ChatWindow userRole="General User" />);
    rerender = renderResult.rerender;
    expect(screen.getByText('Ask a question about HMSREG documentation...')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your question...')).toBeInTheDocument();
  });

  it('shows loading state after sending a message', async () => {
    const renderResult = render(<ChatWindow userRole="Project Manager / Admin" />);
    rerender = renderResult.rerender;

    const input = screen.getByPlaceholderText('Type your question...');
    const button = screen.getByRole('button', { name: /send/i });
    const testMessage = 'Test loading';

    fireEvent.change(input, { target: { value: testMessage } });
    
    await act(async () => {
      fireEvent.click(button); 
    });

    expect(mockSendMessage).toHaveBeenCalledWith(testMessage);
    await waitFor(() => {
      expect(screen.getByText(testMessage)).toBeInTheDocument(); // User message is displayed
      expect(screen.getByText('Connecting...')).toBeInTheDocument(); // Loading indicator
    });
    expect(button).toBeDisabled();
    expect(screen.queryByText(/This is a mock response/)).not.toBeInTheDocument();
  });

  it('displays bot response and citations after successful streaming', async () => {
    const renderResult = render(<ChatWindow userRole="Project Manager / Admin" />);
    rerender = renderResult.rerender;

    const input = screen.getByPlaceholderText('Type your question...');
    const button = screen.getByRole('button', { name: /send/i });
    const testMessage = 'How do I login?';

    fireEvent.change(input, { target: { value: testMessage } });
    
    await act(async () => {
      fireEvent.click(button); 
    });

    expect(mockSendMessage).toHaveBeenCalledWith(testMessage);
    await waitFor(() => {
      expect(screen.getByText(testMessage)).toBeInTheDocument();
      expect(screen.getByText(/This is a mock response about login./)).toBeInTheDocument();
      expect(screen.getByText('Source: Login Guide')).toBeInTheDocument();
    });
    
    expect(screen.queryByText('Connecting...')).not.toBeInTheDocument();
    expect(input).toHaveValue(''); 
    expect(button).toBeDisabled(); // Button should be disabled because input is empty
  });

  it('passes correct messageId and chatSessionId to ChatBubble', async () => {
    const renderResult = render(<ChatWindow userRole="Project Manager / Admin" />);
    rerender = renderResult.rerender;

    const input = screen.getByPlaceholderText('Type your question...');
    const button = screen.getByRole('button', { name: /send/i });
    const testMessage = 'Check IDs';

    fireEvent.change(input, { target: { value: testMessage } });
    await act(async () => {
      fireEvent.click(button); 
    });

    await waitFor(() => {
      // Find the ChatBubble for the assistant message
      const assistantChatBubble = screen.getAllByTestId('mock-chat-bubble').find(
        (element) => element.getAttribute('data-role') === 'assistant'
      );
      
      expect(assistantChatBubble).toBeInTheDocument();
      expect(assistantChatBubble).toHaveAttribute('data-message-id');
      expect(assistantChatBubble).toHaveAttribute('data-chat-session-id');

      // Check if messageId is in the expected format (e.g., starts with 'assistant-')
      expect(assistantChatBubble.getAttribute('data-message-id')).toMatch(/^assistant-/);
      // chatSessionId is generated by Date.now().toString() so it should be a number string
      expect(assistantChatBubble.getAttribute('data-chat-session-id')).toMatch(/^\d+$/);
    });
  });
});