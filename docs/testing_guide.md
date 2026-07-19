# Testing Guide

This document outlines the manual API testing performed using Swagger UI.

---

# Test Scenario 1 — User Creation

1. Create a new user.
2. Verify that the user is successfully created.
3. Verify the initial wallet balance is zero.

Expected Result

- User is created successfully.
- Wallet balance is initialized to 0.

---

# Test Scenario 2 — Sale Creation

1. Create a new sale.
2. Verify that the sale is created.
3. Verify that 10% of the commission is credited to the user's wallet.
4. Verify that an ADVANCE transaction is recorded.

Expected Result

- Sale status is PENDING.
- Advance commission is credited exactly once.

---

# Test Scenario 3 — Sale Approval

1. Approve the pending sale.
2. Verify that the remaining commission is credited.
3. Verify that a PAYOUT transaction is recorded.

Expected Result

- Sale status becomes APPROVED.
- User wallet reflects the full commission amount.

---

# Test Scenario 4 — Successful Withdrawal

1. Create a withdrawal request.
2. Verify sufficient wallet balance validation.
3. Verify wallet balance is deducted.
4. Verify a WITHDRAWAL transaction is created.
5. Verify `last_withdrawal_at` is updated.

Expected Result

- Withdrawal is completed successfully.
- Wallet balance decreases by the withdrawal amount.

---

# Test Scenario 5 — 24-Hour Withdrawal Rule

1. Create a successful withdrawal.
2. Immediately attempt another withdrawal.

Expected Result

- The second withdrawal request is rejected.
- The API returns an error indicating that the user must wait until the 24-hour cooldown period has expired.

---

# Test Scenario 6 — Failed Withdrawal Recovery

1. Mark a completed withdrawal as FAILED.
2. Verify that the withdrawn amount is refunded.
3. Verify that a RECOVERY transaction is created.
4. Verify that `last_withdrawal_at` is reset.
5. Verify that the withdrawal is marked as recovered.

Expected Result

- Wallet balance is fully restored.
- Recovery transaction is successfully recorded.
- User becomes immediately eligible for another withdrawal.

---

# Test Scenario 7 — Withdrawal After Recovery

1. Immediately create another withdrawal after recovery.

Expected Result

- The withdrawal request succeeds without waiting for 24 hours.

---

# Test Scenario 8 — Duplicate Recovery Prevention

1. Attempt to recover the same withdrawal again.

Expected Result

- The request is rejected.
- Duplicate wallet refunds are prevented.