# SG-Gruppe-3-Kun
Repository for SG-Gruppe-3-Kun - IBE160 Programmering med KI.

## State Management

This project uses a hybrid approach to state management, leveraging both the built-in React Context API and the Zustand library. This approach allows us to use the right tool for the right job, resulting in a more performant and maintainable application.

### Zustand

Zustand is used for managing frequently updated, global state. This includes:

*   The chat conversation history (messages)
*   The current user input
*   Loading states (e.g., when the bot is "typing")

Zustand is used for this type of state because it is highly performant and prevents unnecessary re-renders of components.

### React Context API

The React Context API is used for managing global state that changes infrequently. This includes:

*   The current theme (e.g., light or dark mode)
*   User session information
*   Feature flags

The Context API is used for this type of state because it is built into React and is simple to use for data that does not change often.
