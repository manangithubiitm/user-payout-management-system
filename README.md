# User Payout Management System

A FastAPI-based backend service that manages users, sales, commissions, wallet balances, withdrawals, and payout recovery workflows using MongoDB.

The project follows a layered architecture with separate models, repositories, services, and API routes to keep the business logic organized, maintainable, and easy to extend.

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
- PyMongo
- Pydantic
- Uvicorn

---

## Project Structure

```text
.
├── app/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Documentation

Detailed project documentation is available in the `docs/` directory.

- Project Overview
- System Architecture
- Low Level Design (LLD)
- API Design
- Business Rules
- Database Design
- Testing Guide
- Assumptions

---

## API Endpoints

### Users

- `POST /users`
- `GET /users/{user_id}`

### Sales

- `POST /sales`
- `GET /sales/{sale_id}`
- `POST /sales/{sale_id}/approve`
- `POST /sales/{sale_id}/reject`

### Withdrawals

- `POST /withdrawals`
- `GET /withdrawals/{withdrawal_id}`
- `POST /withdrawals/{withdrawal_id}/status`

---

## Business Logic

### Sale Creation

- Creates a sale record.
- Immediately credits 10% of the commission to the user's wallet.

### Sale Approval

- Credits the remaining 90% commission.
- Updates the user's wallet balance.
- Records the payout transaction.

### Withdrawal

- Validates wallet balance.
- Enforces a 24-hour cooldown between withdrawals.
- Deducts the withdrawal amount from the wallet.
- Records the withdrawal transaction.

### Failed Payout Recovery

If a withdrawal is marked as **FAILED** or **CANCELLED**, the system:

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

Run the application

```bash
uvicorn app.main:app --reload
```

Open the API documentation

```
http://127.0.0.1:8000/docs
```

---

## Author

Developed by **Manan Tilwani**