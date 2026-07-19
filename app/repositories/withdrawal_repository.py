from typing import Any, Dict, List

from app.config.database import db
from app.repositories.base_repository import BaseRepository


class WithdrawalRepository(BaseRepository):
    def __init__(self):
        super().__init__(db.withdrawals)

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Find all withdrawals with the given status.

        Args:
            status: The withdrawal status to filter by.

        Returns:
            A list of matching withdrawals.
        """
        return self.find_many({"status": status})
    
    def update_withdrawal(self, withdrawal_id: str, update_data: Dict[str, Any]) -> int:
        """
        Update a withdrawal by its ID.
        """
        return self.update_one(
            {"_id": self._object_id(withdrawal_id)},
            update_data
        )