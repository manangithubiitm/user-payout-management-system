from decimal import Decimal
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import (Transaction, ReferenceType, TransactionType, TransactionStatus)

#Initialize Repository
class TransactionService:
    def __init__(self):
        self.transaction_repository = TransactionRepository()
    
    # Record a transaction
    def create_transaction(
        self, 
        user_id: str, 
        reference_type: ReferenceType, 
        reference_id: str, 
        transaction_type: TransactionType, 
        amount: Decimal, 
        status: TransactionStatus = TransactionStatus.COMPLETED,
    ) -> str:
        """
        Create a transaction record
        """
        if amount <= Decimal("0"):
            raise ValueError("Transaction amount must be greater than zero.")
        transaction = Transaction(
            user_id=user_id,
            reference_type=reference_type,
            reference_id=reference_id,
            transaction_type=transaction_type,
            amount=amount,
            status=status
        )
        transaction_data = transaction.model_dump()
        try:
            return self.transaction_repository.create(transaction_data)
        except Exception as e:
            raise RuntimeError(
                f"Failed to create transaction: {e}"
            ) 

# For converting Pydantic model into a dictionary before inserting it into MongoDB, we use model_dump() method 