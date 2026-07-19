# User Payout Management System

A FastAPI-based backend service that manages users, sales, commissions, wallet balances, withdrawals, and payout recovery workflows using MongoDB.

---

## Features

- User management
- Sales creation
- 10% advance commission credit
- Sale approval and remaining commission payout
- Wallet management
- Withdrawal requests
- 24-hour withdrawal restriction
- Failed/Cancelled payout recovery
- Automatic wallet refund
- Recovery transaction logging
- RESTful API with Swagger UI

---

## Tech Stack

- Python 3.x
- FastAPI
- MongoDB
- Pydantic
- PyMongo
- Uvicorn

---

## Project Structure

```
app/
├── models/
├── repositories/
├── routes/
├── schemas/
├── services/
├── utils/
└── main.py
```

---

## API Endpoints

### Users

- POST /users
- GET /users/{user_id}

### Sales

- POST /sales
- GET /sales/{sale_id}
- POST /sales/{sale_id}/approve

### Withdrawals

- POST /withdrawals
- GET /withdrawals/{withdrawal_id}
- POST /withdrawals/{withdrawal_id}/status

### Transactions

- GET /transactions

---

## Business Logic

### Sale Creation

- Creates a sale record.
- Immediately credits 10% of the commission to the user's wallet.

### Sale Approval

- Credits the remaining 90% commission.
- Updates wallet balance.
- Records transactions.

### Withdrawal

- Validates wallet balance.
- Enforces a 24-hour cooldown between withdrawals.
- Debits the wallet.
- Records withdrawal transactions.

### Failed Payout Recovery

If a withdrawal is marked as:

- FAILED
- CANCELLED

The system:

- Refunds the wallet balance.
- Creates a RECOVERY transaction.
- Marks the withdrawal as recovered.
- Clears the withdrawal cooldown, allowing an immediate new withdrawal.

---

## Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Author

Developed by **Manan Tilwani**