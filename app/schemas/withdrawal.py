from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from app.models.withdrawal import WithdrawalStatus

class WithdrawalBase(BaseModel):
    user_id: str
    amount: Decimal

class WithdrawalCreate(WithdrawalBase):
    """
    Request schema for requesting a withdrawal.
    """
    pass

class WithdrawalStatusUpdate(BaseModel):
    """
    Request schema for updating the payout status.
    """
    status: WithdrawalStatus

class WithdrawalResponse(WithdrawalBase):
    """
    Response schema for returning withdrawal details.
    """
    id: str
    status: WithdrawalStatus
    recovered: bool
    requested_at: datetime
    processed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )