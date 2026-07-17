from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import EmailStr, Field
from app.models.base import BaseDocument

class User(BaseDocument):
    user_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    wallet_balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    last_withdrawal_at: Optional[datetime] = None
