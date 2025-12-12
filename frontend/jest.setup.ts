import '@testing-library/jest-dom';
import 'whatwg-fetch'; // Polyfill for fetch, Headers, Response, etc.

// Mock scrollIntoView
window.HTMLElement.prototype.scrollIntoView = jest.fn();

jest.mock('react-markdown', () => (props: { children: any }) => {
  return props.children;
});