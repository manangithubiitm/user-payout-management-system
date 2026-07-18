from datetime import datetime, timedelta
from decimal import Decimal
from app.models.withdrawal import Withdrawal, WithdrawalStatus
from app.models.transaction import (ReferenceType, TransactionType)
from app.repositories.withdrawal_repository import WithdrawalRepository
from app.services.user_service import UserService
from app.services.transaction_service import TransactionService

class WithdrawalService:
    def __init__(self):
        self.withdrawal_repository = WithdrawalRepository()
        self.user_service = UserService()
        self.transaction_service = TransactionService()
    
    def get_withdrawal_by_id(self, withdrawal_id: str) -> dict:
        """
        Retrieve a withdrawal by ID.
        """
        withdrawal = self.withdrawal_repository.find_by_id(withdrawal_id)
        if withdrawal is None:
            raise ValueError("Withdrawal not found.")
        
        return withdrawal
    
    def request_withdrawal(self, withdrawal: Withdrawal) -> str:
        """
        Request a withdrawal.
        Args:
            withdrawal: Withdrawal Object
        Returns:
            Created withdrawal ID.
        """
        # Step-1: Verify user exists
        user = self.user_service.get_user_by_id(withdrawal.user_id)
        # Step-2: Validate withdrawal amount
        if withdrawal.amount <= Decimal("0"):
            raise ValueError("Withdrawal amount must be greater than zero.")
        # Step-3: Check wallet balance
        wallet_balance = Decimal(user["wallet_balance"])
        if wallet_balance < withdrawal.amount:
            raise ValueError("Insufficient wallet balance.")
        # Step-4: Check 24-hour rule
        last_withdrawal = user.get("last_withdrawal_at")
        if last_withdrawal is not None:
            elapsed = datetime.utcnow() - last_withdrawal
            if elapsed < timedelta(hours=24):
                raise ValueError("Withdrawal allowed only once every 24 hours.")
            
        # Step-5: Create withdrawal
        withdrawal_id = self.withdrawal_repository.create(withdrawal.model_dump())
        # Step-6: Debit wallet
        self.user_service.debit_wallet(withdrawal.user_id, withdrawal.amount)
        # Step-7: Record transaction
        self.transaction_service.create_transaction(
            user_id=withdrawal.user_id,
            reference_type=ReferenceType.WITHDRAWAL,
            reference_id=withdrawal_id,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=withdrawal.amount,
        )
        # Step-8: Update last withdrawal time
        self.user_service.update_last_withdrawal_time(
            withdrawal.user_id,
            datetime.utcnow(),
        )
        
        # Step-9: Mark withdrawal completed
        updated = self.withdrawal_repository.update_withdrawal(
            withdrawal_id,
            {
                "status": WithdrawalStatus.COMPLETED.value,
                "processed_at": datetime.utcnow(),
            },
        )
        if updated == 0:
            raise RuntimeError("Failed to update withdrawal.")
        
        return withdrawal_id