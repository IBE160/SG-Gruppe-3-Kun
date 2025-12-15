// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import createMiddleware from 'next-intl/middleware';
import { locales, defaultLocale } from './lib/i18n/config';

const intlMiddleware = createMiddleware({
  locales,
  defaultLocale,
  localePrefix: 'as-needed', // Don't add /en prefix for default
});

export async function middleware(request: NextRequest) {
  // Handle Logfire tracing
  if (request.nextUrl.pathname === '/client-traces') {
    const logfireToken = process.env.LOGFIRE_TOKEN;

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

  // Handle locale routing with preference detection
  const cookieLocale = request.cookies.get('preferred-locale')?.value;

  if (cookieLocale && locales.includes(cookieLocale as any)) {
    const url = request.nextUrl.clone();

    // Redirect if user prefers non-default locale
    if (!url.pathname.startsWith(`/${cookieLocale}`) && cookieLocale !== defaultLocale) {
      url.pathname = `/${cookieLocale}${url.pathname}`;
      return Response.redirect(url);
    }
  }

  return intlMiddleware(request);
}

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)', '/client-traces']
};
