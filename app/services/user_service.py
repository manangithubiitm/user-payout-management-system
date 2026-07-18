from decimal import Decimal
from app.models.user import User
from datetime import datetime
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def create_user(self, user: User) -> str:
        """
        Create a new user.
        """
        exisiting_user = self.user_repository.find_by_email(user.email)
        if exisiting_user:
            raise ValueError("A user with this email already exists.")
        return self.user_repository.create(user.model_dump())
    
    def get_user_by_id(self, user_id: str) -> dict:
        """
        Retrieve a user by ID.
        """
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        return user
    
    def get_user_by_email(self, email: str) -> dict:
        """
        Retrieve a user by email.
        """

        user = self.user_repository.find_by_email(email)

        if user is None:
            raise ValueError("User not found.")

        return user
    
    def update_wallet_balance(self, user_id: str, new_balance: Decimal) -> None:
        """
        Update a user's wallet balance.
        """
        if new_balance < Decimal("0"):
            raise ValueError("Wallet balance cannot be negative.")
        self.get_user_by_id(user_id)

        updated = self.user_repository.update_wallet_balance(user_id, new_balance)
        if updated == 0:
            raise RuntimeError("Failed to update the wallet balance.")

    def credit_wallet(self, user_id: str, amount: Decimal) -> None:
        """
        Credit the specified amount to the user's wallet.
        Args:
            user_id: The user's ID,
            amount: Amount to credit.
        """
        if amount <= Decimal("0"):
            raise ValueError("Credit amount must be greater than zero.")
        user = self.get_user_by_id(user_id)
        current_balance = Decimal(user["wallet_balance"])
        new_balance = current_balance + amount
        self.update_wallet_balance(user_id, new_balance)
    
    def debit_wallet(self, user_id: str, amount: Decimal) -> None:
        """
        Debit the specified amount from the user's wallet.

        Args:
            user_id: The user's ID,
            amount: Amount to debit.
        """
        if amount <= Decimal("0"):
            raise ValueError("Debit amount must be greater than zero.")
        user = self.get_user_by_id(user_id)
        current_balance = Decimal(user["wallet_balance"])
        if current_balance < amount:
            raise ValueError("Insufficient wallet balance.")
        new_balance = current_balance - amount
        self.update_wallet_balance(user_id, new_balance)





    def user_exists(self, user_id: str) -> bool:
        """
        Check whether a user exists.
        """
        return self.user_repository.find_by_id(user_id) is not None
    
    def update_last_withdrawal_time(self, user_id: str, withdrawal_time: datetime,) -> None:
        """
        Update the user's last withdrawal time.
        """
        updated = self.user_repository.update_last_withdrawal_time(
            user_id,
            withdrawal_time,
        )

        if updated == 0:
            raise RuntimeError(
                "Failed to update the last withdrawal time."
            )