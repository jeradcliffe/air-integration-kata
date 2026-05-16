# AIR Integration Kata

## Quick Start

Run the mock APIs and test suite:

```bash
node start-and-test.js
```

This starts both the Event Stream API (port 3000) and Users & Sessions API (port 3001), then validates connectivity.

## Documentation

- **[Exercise Goals](./KATA_EXERCISE_GOALS.md)** — Overview of the four-week progression, learning objectives, and
  expected output format for user journeys.

- **[Event Stream API](./external/event-stream/API_EVENT_STREAM.md)** — Session-level event tracking. Returns events (
  VIEW, ADD_TO_CART, etc.) with timestamps and properties.

- **[Users & Sessions API](./external/users-and-sessions/API_USERS_AND_SESSIONS.md)** — User-scoped context. Maps
  sessions to users, provides cart history, and point-in-time cart state queries.

## Exercise

Build a service that joins session-level events with user-level context to produce user journeys showing what users
viewed, their account state, cart contents, and purchase history.
