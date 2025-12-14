// components/LogfireInitializer.tsx
'use client'; // This directive marks the component as a Client Component

import { useEffect } from 'react';
import dynamic from 'next/dynamic';
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';

// Dynamically import logfire-browser to ensure it only runs on the client
const LogfireBrowser = dynamic(
  async () => {
    const logfire = await import('@pydantic/logfire-browser');
    return function LogfireInitializerComponent() {
      useEffect(() => {
        const url = new URL(window.location.href);
        url.pathname = '/client-traces'; // This should match your middleware path

        logfire.configure({
          traceUrl: url.toString(),
          serviceName: 'my-nextjs-app-client',
          serviceVersion: '0.1.0',
          instrumentations: [getWebAutoInstrumentations()],
          diagLogLevel: logfire.DiagLogLevel.ALL, // Use ALL for development/troubleshooting
        });

        // Example of a manual span
        logfire.info('Logfire browser initialized');

        return () => {
          // Optional: Shutdown Logfire on component unmount if needed
          // logfire.shutdown();
        };
      }, []);
      return null; // This component doesn't render anything
    };
  },
  { ssr: false } // Important: disable server-side rendering for this component
);

export default LogfireBrowser;
