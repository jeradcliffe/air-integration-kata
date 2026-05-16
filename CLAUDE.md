# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is a learning kata. The goal is to build a service that joins two existing mock APIs to produce **user journeys** as JSON. The exercise repeats weekly with fresh implementations — the learning target is the agentic development system, not the code itself.

## Hard Constraints

**Do not modify anything under `external/`.** The two mock APIs and their data are off-limits. This includes `external/event-stream/` and `external/users-and-sessions/`, their `server.js` files, route files, and data files. Hooks enforce this — attempts to edit those paths will be blocked.

## Running the Mock APIs

Start both APIs and validate connectivity:

```bash
node start-and-test.js
```

This launches both servers and runs smoke tests. Keep this running in a separate terminal while developing.

| API | Port | Base URL |
|---|---|---|
| Event Stream | 3000 | `http://localhost:3000` |
| Users & Sessions | 3001 | `http://localhost:3001` |

Both expose `GET /health`.

## API Summary

### Event Stream API (`localhost:3000`)

```
GET /events/{sessionId}
```

Returns an array of events for a session. Each event has `eventType`, `timestamp`, `sessionId`, and `properties`. Event types: `VIEW`, `ADD_TO_CART`, `REMOVE_FROM_CART`, `PURCHASE`. Returns 404 if no events for that session.

### Users & Sessions API (`localhost:3001`)

```
GET /users                              → { users: string[] }
GET /users/session/{sessionId}          → { userId, sessionId }
GET /users/{userId}/sessions            → { userId, sessions: string[] }
GET /users/{userId}/cart                → { userId, cartHistory: CartSnapshot[] }
GET /users/{userId}/cart?timestamp=N    → cart state at exact timestamp
```

Cart lookup by timestamp matches exact values only — if no snapshot exists at that timestamp, it returns 404.

## Data Set

25 users (Alice–Yara), each with one session (session-001 through session-025). The large dataset (`large-events.json`) includes intentional edge cases for validation testing: absurd quantities (250–5000), invalid events (missing `productId`, negative prices, zero/negative quantities, far-future timestamps), and special sessions (session-023 has only `REMOVE_FROM_CART`; session-025 has only `VIEW` and `PURCHASE`).

See `external/event-stream/data/LARGE_EVENTS_INDEX.md` for a full breakdown by session.

## Integration Pattern

To produce a user journey for all users:

1. `GET /users` → list of userIds
2. For each userId: `GET /users/{userId}/sessions` → their session IDs
3. For each sessionId: `GET /events/{sessionId}` → raw events
4. `GET /users/{userId}/cart` → cart history (for context alongside events)
5. Join and produce the output shape from `KATA_EXERCISE_GOALS.md`

## Expected Output Shape

```json
{
  "userId": "Alice",
  "journeys": [
    {
      "sessionId": "session-001",
      "startTime": 1620000000,
      "endTime": 1620000090,
      "events": [...],
      "cartStateChanges": [...]
    }
  ]
}
```

Full schema in `KATA_EXERCISE_GOALS.md`.

## Weekly Exercise Phases

The implementation is deleted and restarted each week. You may keep skills, hooks, workflows, and agent definitions across resets.

- **Week 1**: Discovery & context capture — understand the system, prevent agents from touching the mock APIs
- **Week 2**: Design & feasibility — produce a design, validate it is achievable with the available APIs
- **Week 3**: Implementation & proof — TDD, ensure the implementation is actually tested
- **Week 4**: Optimization — reduce cost, time, and required user expertise in the agentic system
