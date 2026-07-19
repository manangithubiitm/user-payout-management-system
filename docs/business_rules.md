# Business Rules

## Sale Creation

- A new sale is initially created with a **PENDING** status.
- Immediately after sale creation, **10% of the commission** is credited to the user's wallet as an advance.
- An **ADVANCE** transaction is recorded.
- The advance is paid only once using the `advance_paid` flag.

---

## Sale Approval

- A sale can only be approved once.
- The remaining **90% of the commission** is credited to the user's wallet.
- A **PAYOUT** transaction is recorded.
- The sale is marked as reconciled to prevent duplicate payouts.

---

## Sale Rejection

- If a sale is rejected after an advance payout, the previously credited advance commission is deducted from the user's wallet.
- An **ADJUSTMENT** transaction is recorded.
- The sale is marked as reconciled.

---

## Withdrawal

- A user must have sufficient wallet balance before requesting a withdrawal.
- Only **one withdrawal is permitted within a rolling 24-hour period**.
- Any withdrawal request made before the 24-hour cooldown expires is rejected.
- On a successful withdrawal:
  - The requested amount is deducted from the wallet.
  - A **WITHDRAWAL** transaction is recorded.
  - The user's `last_withdrawal_at` timestamp is updated.

---

## Failed or Cancelled Withdrawal

When a completed withdrawal is marked as **FAILED** or **CANCELLED**:

- The withdrawn amount is refunded to the user's wallet.
- A **RECOVERY** transaction is recorded.
- The user's `last_withdrawal_at` timestamp is cleared.
- The withdrawal is marked as recovered.
- The same withdrawal cannot be recovered more than once.
- The user can immediately create a new withdrawal request without waiting for the previous 24-hour cooldown.

---

## Financial Ledger

Every monetary movement is recorded as a transaction to maintain a complete financial audit trail.

Transaction types include:

- ADVANCE
- PAYOUT
- ADJUSTMENT
- WITHDRAWAL
- RECOVERY