# Responsibility: Initialize the database when the application starts
from app.config.database import db
COLLECTIONS = [
    "users",
    "sales",
    "withdrawals",
    "transactions"
]
def create_collections():
    existing_collections = db.list_collection_names()
    for collection in COLLECTIONS:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Created collection: {collection}")
        else:
            print(f"Collection already exists: {collection}")


def create_indexes():
    # Users collection
    db.users.create_index("email", unique=True)

    # Sales Collection
    db.sales.create_index("user_id")
    db.sales.create_index("status")
    db.sales.create_index([("status", 1), ("advance_paid", 1)])
    db.sales.create_index([("status", 1), ("reconciled", 1)])

    # Withdrawals Collection
    db.withdrawals.create_index([("user_id", 1), ("requested_at", -1)])

    # Transactions Collection
    db.transactions.create_index("user_id")
    db.transactions.create_index([("reference_type", 1), ("reference_id", 1)])
    db.transactions.create_index("transaction_type")

    print("Database indexes created successfully.")