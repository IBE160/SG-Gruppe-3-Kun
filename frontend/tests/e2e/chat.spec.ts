import { test, expect } from '@playwright/test';

test.describe('Chat Flow', () => {
  test('Complete user journey: Select role, ask question, receive stream', async ({ page }) => {
    // 1. Mock the API route to avoid backend dependency
    await page.route('/api/chat', async (route) => {
      // We need to verify the request body if we want to be strict
      const request = route.request();
      const postData = request.postDataJSON();
      expect(postData.message).toBe('How do I login?');
      expect(postData.user_role).toBe('Construction Worker');

      // Respond with a stream
      // Playwright route.fulfill doesn't easily support streams unless we use a buffer or similar,
      // but for this test, we can simulate the frontend reaction to a stream by 
      // just returning the SSE format in the body.
      // However, the frontend uses ReadableStream on the response body.
      // Ideally, we'd use a real server or a more advanced mock.
      // But standard route.fulfill with text/event-stream content type works for many SSE clients.
      
      const streamContent = `data: {"type": "token", "content": "To "}\n\ndata: {"type": "token", "content": "login..."}\n\ndata: [DONE]\n\n`;
      
      await route.fulfill({
        status: 200,
        contentType: 'text/event-stream',
        body: streamContent,
      });
    });

    // 2. Visit the homepage
    await page.goto('/');

    // 3. Select Role
    // Wait for the role selector to appear
    await expect(page.getByRole('button', { name: 'Construction Worker' })).toBeVisible();
    await page.getByRole('button', { name: 'Construction Worker' }).click();

    // 4. Verify Chat Interface loaded (Desktop)
    // We target the desktop view specifically as Playwright default viewport is wide
    const chatContainer = page.getByTestId('desktop-right-col');
    const input = chatContainer.getByPlaceholder('Type your question...');
    await expect(input).toBeVisible();

    // 5. Send a message
    await input.fill('How do I login?');
    await chatContainer.getByRole('button', { name: 'Send' }).click();

    // 6. Verify User Message
    await expect(chatContainer.getByText('How do I login?')).toBeVisible();

    // 7. Verify Assistant Response (from mock)
    // The mock returns "To login..."
    // Frontend appends tokens: "To " + "login..." = "To login..."
    await expect(chatContainer.getByText('To login...')).toBeVisible();

    // 8. Mock Feedback API
    await page.route('/api/v1/feedback', async (route) => {
      expect(route.request().method()).toBe('POST');
      const postData = route.request().postDataJSON();
      expect(postData.rating).toBe('thumbs_up');
      await route.fulfill({ status: 201 });
    });

    // 9. Give Feedback
    // Wait for feedback buttons to appear (they appear with the assistant message)
    await expect(chatContainer.getByRole('button', { name: 'Thumbs up' })).toBeVisible();
    await chatContainer.getByRole('button', { name: 'Thumbs up' }).click();
    
    // 10. Verify Feedback State
    await expect(chatContainer.getByText('👍 Thanks!')).toBeVisible();
  });
});
