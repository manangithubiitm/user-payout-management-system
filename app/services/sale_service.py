from decimal import Decimal
from app.models.sale import Sale, SaleStatus
from app.models.transaction import (ReferenceType, TransactionType)
from app.repositories.sale_repository import SaleRepository
from app.services.user_service import UserService
from app.services.transaction_service import TransactionService

class SaleService:
    def __init__(self):
        self.sale_repository = SaleRepository()
        self.user_service = UserService()
        self.transaction_service = TransactionService()
    
    def get_sale_by_id(self, sale_id: str) -> dict:
        """
        Retrieve a sale by ID.
        """
        sale = self.sale_repository.find_by_id(sale_id)
        if sale is None:
            raise ValueError("Sale not found")
        return sale
    
    # Helper method to pay 10% advance payout for every sale
    def _calculate_advance_commission(self, commission_amount: Decimal) -> Decimal:
        """
        Calculate the advance commission (10% of the commission amount).
        Args:
            commission_amount: Total commission earned.
        Returns:
            Advance commission amount.
        """
        return commission_amount * Decimal("0.10")
    
    def create_sale(self, sale: Sale) -> str:
        """
        Create a new sale and pay the advance commission.

        Args:
            sale: Sale object
        Returns:
            The created sale ID.
        """
        # Step-1: Verify that the user exists
        if not self.user_service.user_exists(sale.user_id):
            raise ValueError("User not found.")
        
        # Step - 2: Validate commission amount
        if sale.commission_amount <= Decimal("0"):
            raise ValueError("Commission amount must be greater than zero.")
        
        # Step-3: Create the sale
        sale_id = self.sale_repository.create(sale.model_dump())

        # Step-4: Calculate advance commission
        advance_amount = self._calculate_advance_commission(sale.commission_amount)

        # Step-5: Credit the user's wallet
        self.user_service.credit_wallet(sale.user_id, advance_amount)

        # Step-6: Record the advance transaction
        self.transaction_service.create_transaction(
            user_id=sale.user_id,
            reference_type=ReferenceType.SALE,
            reference_id=sale_id,
            transaction_type=TransactionType.ADVANCE,
            amount=advance_amount,
        )
        # Step-7: Mark advance as paid
        updated = self.sale_repository.update_sale(sale_id, { "advance_paid": True, },)
        if updated == 0:
            raise RuntimeError("Failed to update the sale")
        
        return sale_id
    
    def approve_sale(self, sale_id: str) -> None:
        """
        Approve a sale and pay the remaining commission.
        Args:
            sale_id: Sale ID.
        """
        sale = self.get_sale_by_id(sale_id)
        if sale["status"] != SaleStatus.PENDING.value:
            raise ValueError("Only pending sales can be approved.")
        if not sale["advance_paid"]:
            raise ValueError("Advance commission has not been paid.")
        if sale["reconciled"]:
            raise ValueError("Sale has already been reconciled.")
        remaining_commission = (
            Decimal(sale["commission_amount"]) - self._calculate_advance_commission(
                Decimal(sale["commission_amount"])
            )
        )
        self.user_service.credit_wallet(
            sale["user_id"],
            remaining_commission
        )
        self.transaction_service.create_transaction(
            user_id=sale["user_id"],
            reference_type=ReferenceType.SALE,
            reference_id=sale_id,
            transaction_type=TransactionType.FINAL,
            amount=remaining_commission,
        )
        updated = self.sale_repository.update_sale(
            sale_id,
            {
                "status": SaleStatus.APPROVED.value,
                "reconciled": True
            },
        )
        if updated == 0:
            raise RuntimeError("Failed to approve the sale.")

    def reject_sale(self, sale_id: str) -> None:
        """
        Reject a sale and recover the advance commission.
        Args:
            sale_id: Sale ID.
        """    
        sale = self.get_sale_by_id(sale_id)
        if sale["status"] != SaleStatus.PENDING.value:
            raise ValueError("Only pending sales can be rejected.")

        if not sale["advance_paid"]:
            raise ValueError("Advance commission has not been paid.")
        
        if sale["reconciled"]:
            raise ValueError("Sale has already been reconciled.")
        advance_amount = self._calculate_advance_commission(
            Decimal(sale["commission_amount"])
        )
        self.user_service.debit_wallet(
            sale["user_id"],
            advance_amount,
        )
        self.transaction_service.create_transaction(
            user_id=sale["user_id"],
            reference_type=ReferenceType.SALE,
            reference_id=sale_id,
            transaction_type=TransactionType.ADJUSTMENT,
            amount=advance_amount,
        )
        updated = self.sale_repository.update_sale(
            sale_id,
            {
                "status": SaleStatus.REJECTED.value,
                "reconciled": True,
            },
        )
        if updated == 0:
            raise RuntimeError("Failed to reject the sale.")