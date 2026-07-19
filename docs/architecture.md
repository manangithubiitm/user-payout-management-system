# System Architecture

The application follows a layered architecture.

Client
↓

API Routes

↓

Services

↓

Repositories

↓

MongoDB

---

## Layers

### Models

Represent MongoDB documents.

### Schemas

Validate API requests and responses.

### Routes

Expose REST endpoints.

### Services

Contain business logic.

### Repositories

Interact with MongoDB.

### Utilities

Common helper functions such as response mapping.

---

## Benefits

- Separation of concerns
- Easier testing
- Easier maintenance
- Better scalability