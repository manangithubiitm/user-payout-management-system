from app.config.database import db
from app.repositories.base_repository import BaseRepository
from typing import Any, Dict, List

class SaleRepository(BaseRepository):
    def __init__(self):
        super().__init__(db.sales)

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Find all sales with the given status.

        Args:
            status: The sale status to filter by.
        
        Returns:
            A list of matching sales.
        """
        return self.find_many({"status": status})
    
    def update_sale(self, sale_id: str, update_data: Dict[str, Any],) -> int:
        """
        Update a sale by its ID.

        Args:
            sale_id: Sale ID.
            update_data: Fields to update.
        
        Returns:
            Number of modified documents.
        """
        return self.update_one(
            {"_id": self._object_id(sale_id)},
            update_data,
        )