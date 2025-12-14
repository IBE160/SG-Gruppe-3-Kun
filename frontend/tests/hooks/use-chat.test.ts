import { renderHook, act } from '@testing-library/react';
import { useChat } from '@/hooks/use-chat';
import { TextEncoder } from 'util';

// Mock global fetch
global.fetch = jest.fn();
// Polyfill TextDecoder if needed (JSDOM usually has it, but TextEncoder might need import in some envs)
// But Jest JSDOM usually handles it. Explicit import from 'util' for node env just in case.

describe('useChat', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should handle citation events', async () => {
    const encoder = new TextEncoder();
    const tokenData = JSON.stringify({ type: "token", content: "Hello" });
    const citationData = JSON.stringify({ type: "citation", content: [{ title: "Source", url: "http://example.com" }] });

    const mockReader = {
      read: jest.fn()
        .mockResolvedValueOnce({ done: false, value: encoder.encode(`data: ${tokenData}\n\n`) })
        .mockResolvedValueOnce({ done: false, value: encoder.encode(`data: ${citationData}\n\n`) })
        .mockResolvedValueOnce({ done: false, value: encoder.encode('data: [DONE]\n\n') })
        .mockResolvedValue({ done: true, value: undefined }),
    };

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      body: {
        getReader: () => mockReader,
      },
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('Hello');
    });

    // Check messages
    const messages = result.current.messages;
    expect(messages).toHaveLength(2); // User + Assistant
    expect(messages[1].content).toBe('Hello');
    expect(messages[1].citations).toEqual([{ title: 'Source', url: 'http://example.com' }]);
  });
});
