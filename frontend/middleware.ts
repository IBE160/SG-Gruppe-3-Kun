// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === '/client-traces') {
    const logfireToken = process.env.LOGFIRE_TOKEN; // Ensure this is securely stored and accessed

    if (!logfireToken) {
      console.error('LOGFIRE_TOKEN is not set in environment variables.');
      return new NextResponse('Logfire token not configured.', { status: 500 });
    }

    const response = await fetch('https://logfire-api.pydantic.dev/collect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${logfireToken}`,
      },
      body: request.body,
    });

    return response;
  }
  return NextResponse.next();
}

export const config = {
  matcher: '/client-traces', // Match requests to this path
};
