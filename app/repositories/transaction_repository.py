from app.config.database import db
from app.repositories.base_repository import BaseRepository

class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(db.transactions)
    
    # Find transactions for a user
    def find_by_user(self, user_id: str):
        """
        Find all transactions for a user.
        """
        return self.find_many({"user_id": user_id})
    
    # Find transactions by reference
    def find_by_reference(self, reference_type: str, referece_id: str):
        """
        Find transactions linked to a sale or withdrawal
        """
        return self.find_many(
            {
                "reference_type": reference_type,
                "reference_id": referece_id
            }
        )