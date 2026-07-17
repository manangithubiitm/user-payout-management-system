# Database Design Document

## Project

**User Payout Management System**

------------------------------------------------------------------------

# 1. Purpose

This document captures the database architecture and design decisions
for the User Payout Management System. It serves as the blueprint for
implementing the MongoDB schema, Python models, business services, and
REST APIs.

------------------------------------------------------------------------

# 2. Design Principles

-   Keep each collection focused on a single responsibility.
-   Avoid unnecessary data duplication.
-   Preserve a complete financial audit trail.
-   Design for extensibility while keeping the assignment scope simple.
-   Prioritize readability and maintainability over premature
    optimization.

------------------------------------------------------------------------

# 3. Collections

## Users

Represents affiliate users who earn commissions and request withdrawals.

**Responsibilities** - Store user profile information. - Maintain
available wallet balance. - Track the last withdrawal timestamp.

**Key Fields** - `_id` - `user_name` - `email` - `wallet_balance` -
`last_withdrawal_at` - `created_at` - `updated_at`

------------------------------------------------------------------------

## Brands

Stores the supported brands available in the platform.

**Responsibilities** - Maintain a centralized list of brands. - Avoid
duplicating brand information across sales.

**Key Fields** - `_id` - `brand_code` - `brand_name` - `is_active` -
`created_at` - `updated_at`

------------------------------------------------------------------------

## Sales

Represents every customer purchase eligible for commission.

**Responsibilities** - Store sale information. - Track approval
status. - Prevent duplicate advance payouts. - Prevent duplicate
reconciliation.

**Key Fields** - `_id` - `user_id` - `brand_id` - `sale_amount` -
`commission_amount` - `status` - `advance_paid` - `reconciled` -
`created_at` - `updated_at`

------------------------------------------------------------------------

## Withdrawals

Represents user withdrawal requests.

**Responsibilities** - Store withdrawal requests. - Track processing
status. - Enforce the 24-hour withdrawal rule.

**Key Fields** - `_id` - `user_id` - `amount` - `status` -
`requested_at` - `processed_at`

------------------------------------------------------------------------

## Transactions

Acts as the financial ledger for every movement of money.

**Responsibilities** - Record advance payouts. - Record final payouts. -
Record adjustments. - Record withdrawals. - Record recovery
transactions.

**Key Fields** - `_id` - `user_id` - `reference_type` - `reference_id` -
`transaction_type` - `amount` - `status` - `created_at`

------------------------------------------------------------------------

# 4. Relationships

-   One User → Many Sales
-   One User → Many Withdrawals
-   One User → Many Transactions
-   One Brand → Many Sales
-   One Sale → Many Transactions
-   One Withdrawal → One or More Transactions (withdrawal/recovery)

------------------------------------------------------------------------

# 5. Business Workflows

## Workflow 1 -- New Sale

1.  Create Sale (Pending).
2.  Calculate 10% advance commission.
3.  Increase wallet balance.
4.  Create Transaction.

## Workflow 2 -- Sale Approved

1.  Update Sale status.
2.  Calculate remaining commission.
3.  Increase wallet balance.
4.  Create Transaction.
5.  Mark Sale as reconciled.

## Workflow 3 -- Sale Rejected

1.  Update Sale status.
2.  Deduct previously paid advance.
3.  Create adjustment Transaction.
4.  Mark Sale as reconciled.

## Workflow 4 -- Withdrawal

1.  Validate 24-hour rule.
2.  Validate wallet balance.
3.  Create Withdrawal.
4.  Deduct wallet balance.
5.  Create Transaction.

## Workflow 5 -- Failed Withdrawal

1.  Mark Withdrawal as failed.
2.  Restore wallet balance.
3.  Create recovery Transaction.

------------------------------------------------------------------------

# 6. Planned Indexes

## Users

-   Unique: `email`

## Brands

-   Unique: `brand_code`

## Sales

-   `user_id`
-   `status`
-   Compound: (`status`, `advance_paid`)
-   Compound: (`status`, `reconciled`)

## Withdrawals

-   Compound: (`user_id`, `requested_at`)

## Transactions

-   `user_id`
-   Compound: (`reference_type`, `reference_id`)
-   `transaction_type`

------------------------------------------------------------------------

# 7. Key Design Decisions

## Decision 1 -- Separate Brands Collection

A dedicated Brands collection was introduced even though the assignment
references only `brand_1`, `brand_2`, and `brand_3`. This normalizes
brand information and allows future attributes (commission rates, logos,
status) without modifying Sales documents.

## Decision 2 -- Transactions as the Financial Ledger

Instead of maintaining a separate Payouts collection, every monetary
movement is recorded in Transactions. This simplifies the design while
preserving a complete financial history.

## Decision 3 -- Wallet Balance in Users

The current available balance is stored with the User to support fast
balance checks. Transactions remain the historical source of truth.

## Decision 4 -- Idempotency Flags

The `advance_paid` and `reconciled` fields in Sales prevent duplicate
payouts if scheduled jobs are retried.

------------------------------------------------------------------------

# 8. Trade-offs

  -----------------------------------------------------------------------
  Decision                Benefit                 Trade-off
  ----------------------- ----------------------- -----------------------
  Separate Brands         Normalized and          One additional lookup
  collection              extensible              

  Transactions ledger     Complete audit trail    Slightly more logic
                                                  when recording events

  Wallet balance on User  Fast reads              Must stay synchronized
                                                  with Transactions

  Idempotency flags       Prevent duplicate       Additional fields to
                          payments                maintain
  -----------------------------------------------------------------------

------------------------------------------------------------------------
