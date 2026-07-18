from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.config.database import db
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(db.users)

    def find_by_email(self, email: str) -> Optional[dict]:
        """
        Find a user by email address.
        """
        return self.find_one({"email": email})
    
    def update_wallet_balance(self, user_id: str, wallet_balance: Decimal) -> int:
        """
        Update the user's wallet balance
        """
        return self.update_one({"_id": self._object_id(user_id)}, {"wallet_balance": wallet_balance})
    
    def update_last_withdrawal_time(self, user_id: str, withdrawal_time: datetime) -> int:
        """
        Update the timestamp of the user's last withdrawal
        """
        return self.update_one(
            {"_id": self._object_id(user_id)},
            {"last_withdrawal_at": withdrawal_time}
        )