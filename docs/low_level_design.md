# Low Level Design

## User Module

Responsibilities

- Create users
- Maintain wallet balance
- Store withdrawal timestamp

Dependencies

- User Repository

---

## Sales Module

Responsibilities

- Create sales
- Approve sales
- Reject sales
- Trigger commission payouts

Dependencies

- User Service
- Transaction Service

---

## Withdrawal Module

Responsibilities

- Validate balance
- Enforce cooldown
- Create withdrawal
- Recover failed payouts

Dependencies

- User Service
- Transaction Service

---

## Transaction Module

Responsibilities

Maintain immutable financial records.

Transaction Types

- ADVANCE
- PAYOUT
- ADJUSTMENT
- WITHDRAWAL
- RECOVERY

---

## Repository Layer

Provides CRUD abstraction over MongoDB.

---

## Service Layer

Contains all business rules and coordinates repository interactions.

---

## Route Layer

Handles HTTP requests and responses.