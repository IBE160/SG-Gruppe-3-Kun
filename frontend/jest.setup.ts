import '@testing-library/jest-dom';
import 'whatwg-fetch'; // Polyfill for fetch, Headers, Response, etc.
import React from 'react'; // Import React

// Mock scrollIntoView
if (typeof window !== 'undefined') {
  window.HTMLElement.prototype.scrollIntoView = jest.fn();
}

jest.mock('react-markdown', () => (props: { children: React.ReactNode }) => {
  return props.children;
});