import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { FeedbackButtons } from '@/components/FeedbackButtons';

// Mock the global fetch function
global.fetch = jest.fn();

describe('FeedbackButtons', () => {
  const defaultProps = {
    messageId: 'msg-123',
    chatSessionId: 'session-456',
  };

  beforeEach(() => {
    // Reset fetch mock before each test
    (fetch as jest.Mock).mockClear();
  });

  it('renders both buttons initially', () => {
    render(<FeedbackButtons {...defaultProps} />);
    expect(screen.getByLabelText('Thumbs up')).toBeInTheDocument();
    expect(screen.getByLabelText('Thumbs down')).toBeInTheDocument();
  });

  it('sends thumbs up feedback on click and shows confirmation', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve({ id: 1, ...defaultProps, rating: 'thumbs_up', created_at: new Date().toISOString() }),
    });

    render(<FeedbackButtons {...defaultProps} />);
    const thumbsUpButton = screen.getByLabelText('Thumbs up');
    fireEvent.click(thumbsUpButton);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('/api/v1/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_session_id: defaultProps.chatSessionId,
        message_id: defaultProps.messageId,
        rating: 'thumbs_up',
      }),
    });

    await waitFor(() => {
      expect(screen.getByText('👍 Thanks!')).toBeInTheDocument();
    });
    expect(thumbsUpButton).not.toBeInTheDocument(); // Buttons should disappear
    expect(screen.queryByLabelText('Thumbs down')).not.toBeInTheDocument();
  });

  it('sends thumbs down feedback on click and shows confirmation', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve({ id: 1, ...defaultProps, rating: 'thumbs_down', created_at: new Date().toISOString() }),
    });

    render(<FeedbackButtons {...defaultProps} />);
    const thumbsDownButton = screen.getByLabelText('Thumbs down');
    fireEvent.click(thumbsDownButton);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('/api/v1/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_session_id: defaultProps.chatSessionId,
        message_id: defaultProps.messageId,
        rating: 'thumbs_down',
      }),
    });

    await waitFor(() => {
      expect(screen.getByText('👎 Thanks!')).toBeInTheDocument();
    });
    expect(thumbsDownButton).not.toBeInTheDocument(); // Buttons should disappear
    expect(screen.queryByLabelText('Thumbs up')).not.toBeInTheDocument();
  });

  it('disables buttons while loading', async () => {
    (fetch as jest.Mock).mockReturnValueOnce(new Promise(() => {})); // Never resolve
    
    render(<FeedbackButtons {...defaultProps} />);
    const thumbsUpButton = screen.getByLabelText('Thumbs up');
    const thumbsDownButton = screen.getByLabelText('Thumbs down');
    
    fireEvent.click(thumbsUpButton);

    expect(thumbsUpButton).toBeDisabled();
    expect(thumbsDownButton).toBeDisabled();

    // Clean up
    (fetch as jest.Mock).mockRestore();
  });

  it('shows error message if submission fails', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));
    
    render(<FeedbackButtons {...defaultProps} />);
    const thumbsUpButton = screen.getByLabelText('Thumbs up');
    fireEvent.click(thumbsUpButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to submit feedback. Please try again.')).toBeInTheDocument();
    });
    expect(screen.queryByText('👍 Thanks!')).not.toBeInTheDocument();
    expect(screen.getByLabelText('Thumbs up')).not.toBeDisabled(); // Buttons re-enabled after error
  });
});
