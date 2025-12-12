import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatWindow } from '@/components/ChatWindow';
import { useChat } from '@/hooks/use-chat';
import { Message, SourceCitation } from '@/hooks/use-chat';

// Mock scrollIntoView
window.HTMLElement.prototype.scrollIntoView = jest.fn();

// Mock the useChat hook
jest.mock('@/hooks/use-chat', () => ({
  useChat: jest.fn(),
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
      // Simulate sending a message: add user message, set loading
      mockMessages = [...mockMessages, { id: Date.now().toString(), role: 'user', content }];
      mockIsLoading = true;
      // Trigger a re-render to reflect the user message and loading state
      act(() => {
        rerender(<ChatWindow userRole="Project Manager" />);
      });
      
      // Simulate API call and streaming delay
      await new Promise(resolve => setTimeout(resolve, 50)); 
      
      // Simulate bot response
      const botResponse: Message = { 
        id: (Date.now() + 1).toString(), 
        role: 'assistant', 
        content: 'This is a mock response about login.', 
        citations: [{ title: 'Login Guide', url: 'https://docs.example.com/login' }] 
      };
      mockMessages = [...mockMessages, botResponse];
      mockIsLoading = false;
      // Trigger a re-render to reflect the bot response
      act(() => {
        rerender(<ChatWindow userRole="Project Manager" />);
      });
    });

    mockUseChat.mockImplementation((userRole: string | null) => ({
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: mockIsLoading,
    }));
  });

  it('renders initial empty state', () => {
    const renderResult = render(<ChatWindow userRole="General User" />);
    rerender = renderResult.rerender; // Capture rerender function
    expect(screen.getByText('Ask a question about HMSREG documentation...')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your question...')).toBeInTheDocument();
  });

  it('shows loading state after sending a message', async () => {
    const renderResult = render(<ChatWindow userRole="Project Manager" />);
    rerender = renderResult.rerender; // Capture rerender function

    const input = screen.getByPlaceholderText('Type your question...');
    const button = screen.getByRole('button', { name: /send/i });
    const testMessage = 'Test loading';

    fireEvent.change(input, { target: { value: testMessage } });
    
    await act(async () => {
      fireEvent.click(button); 
      // After this, mockSendMessage will update mockMessages and mockIsLoading,
      // and call rerender internally. We just need to ensure the act finishes.
    });

    expect(mockSendMessage).toHaveBeenCalledWith(testMessage);
    expect(screen.getByText(testMessage)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText('Connecting...')).toBeInTheDocument();
    });
    expect(button).toBeDisabled();

    // To ensure it stays in loading state for this test, prevent mockSendMessage from finishing.
    // We can do this by overriding mockSendMessage for this test to not simulate bot response.
    // For this test, we only want to see the loading state.
    // So, we just assert that the bot response is NOT there yet.
    expect(screen.queryByText(/This is a mock response/)).not.toBeInTheDocument();
    expect(screen.queryByText('Login Guide')).not.toBeInTheDocument();
  });

  it('displays bot response and citations after successful streaming', async () => {
    const renderResult = render(<ChatWindow userRole="Project Manager" />);
    rerender = renderResult.rerender; // Capture rerender function

    const input = screen.getByPlaceholderText('Type your question...');
    const button = screen.getByRole('button', { name: /send/i });
    const testMessage = 'How do I login?';

    fireEvent.change(input, { target: { value: testMessage } });
    
    await act(async () => {
      fireEvent.click(button); 
      // mockSendMessage will simulate the full stream and rerender.
    });

    expect(mockSendMessage).toHaveBeenCalledWith(testMessage);
    expect(screen.getByText(testMessage)).toBeInTheDocument();
    
    // Use waitFor to ensure final bot message and citations are rendered
    await waitFor(() => {
        expect(screen.getByText(/This is a mock response about login./)).toBeInTheDocument();
        expect(screen.getByText('Login Guide')).toBeInTheDocument();
    });
    expect(screen.getByRole('link', { name: 'Login Guide' })).toHaveAttribute('href', 'https://docs.example.com/login');
    
    expect(screen.queryByText('Connecting...')).not.toBeInTheDocument();
    expect(input).toHaveValue(''); 
    expect(button).toBeDisabled();
  });
});