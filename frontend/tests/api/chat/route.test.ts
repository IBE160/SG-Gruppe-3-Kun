/**
 * @jest-environment node
 */
import { POST } from '@/app/api/chat/route';
import { NextResponse } from 'next/server';

// Mock global fetch
global.fetch = jest.fn();

describe('POST /api/chat', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv, BACKEND_API_URL: 'http://backend-mock:8000' };
    (global.fetch as jest.Mock).mockClear();
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  it('proxies the request to the backend and returns a stream', async () => {
    const mockBody = { message: 'Hello', user_role: 'User' };
    // Create a request with a JSON body
    const req = new Request('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mockBody),
    });

    // Mock successful backend response with a stream
    // In jsdom environment, ReadableStream is available
    const mockStream = new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('data: test\n\n'));
        controller.close();
      },
    });

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      body: mockStream,
      headers: new Headers(),
    });

    const response = await POST(req);

    // Verify backend was called correctly
    expect(global.fetch).toHaveBeenCalledWith('http://backend-mock:8000/api/v1/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mockBody),
    });

    // Verify response is a stream
    expect(response.status).toBe(200);
    expect(response.headers.get('Content-Type')).toBe('text/event-stream');
    expect(response.body).toBeDefined();
  });

  it('handles backend errors gracefully', async () => {
     const mockBody = { message: 'Hello' };
     const req = new Request('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mockBody),
    });

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    });

    const response = await POST(req);

    expect(response.status).toBe(500);
    const json = await response.json();
    expect(json).toEqual({ error: 'Backend error' });
  });
});
