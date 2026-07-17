from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import Field
from app.models.base import BaseDocument

class ReferenceType(str, Enum):
    SALE = "sale"
    WITHDRAWAL = "withdrawal"

class TransactionType(str, Enum):
    ADVANCE = "advance"
    FINAL = "final"
    ADJUSTMENT = "adjustment"
    WITHDRAWAL = "withdrawal"
    RECOVERY = "recovery"

class TransactionStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(BaseDocument):
    user_id: str
    reference_type: ReferenceType
    reference_id: str
    transaction_type: TransactionType
    amount: Decimal
    status: TransactionStatus = TransactionStatus.COMPLETED