from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import Field
from app.models.base import BaseDocument

class WithdrawalStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Withdrawal(BaseDocument):
    user_id: str
    amount: Decimal = Field(..., gt=0)
    status: WithdrawalStatus = WithdrawalStatus.PENDING
    recovered: bool = False
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: datetime | None = Field(default=None)
