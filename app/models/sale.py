from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import Field
from app.models.base import BaseDocument

class SaleStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Sale(BaseDocument):
    user_id: str
    brand_name: str = Field(..., min_length=2, max_length=100)
    sale_amount: Decimal = Field(..., gt=0)
    commission_amount: Decimal = Field(..., ge=0)
    status: SaleStatus = SaleStatus.PENDING
    advance_paid: bool = False
    reconciled: bool = False