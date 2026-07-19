# API Design

The application exposes RESTful APIs for managing users, sales, and withdrawals.

---

# Users

## Create User

```
POST /users
```

Creates a new user.

---

## Get User

```
GET /users/{user_id}
```

Retrieves user details, including the current wallet balance.

---

# Sales

## Create Sale

```
POST /sales
```

Creates a new sale and credits the advance commission.

---

## Get Sale

```
GET /sales/{sale_id}
```

Retrieves sale details.

---

## Approve Sale

```
POST /sales/{sale_id}/approve
```

Approves a sale and credits the remaining commission.

---

## Reject Sale

```
POST /sales/{sale_id}/reject
```

Rejects a sale and reverses any previously paid advance commission.

---

# Withdrawals

## Create Withdrawal

```
POST /withdrawals
```

Creates a withdrawal request after validating wallet balance and the 24-hour withdrawal rule.

---

## Get Withdrawal

```
GET /withdrawals/{withdrawal_id}
```

Retrieves withdrawal details.

---

## Update Withdrawal Status

```
POST /withdrawals/{withdrawal_id}/status
```

Marks a completed withdrawal as **FAILED** or **CANCELLED** and automatically performs the recovery workflow.