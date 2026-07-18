from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from app.models.sale import SaleStatus

class SaleBase(BaseModel):
    user_id: str
    brand_name: str
    sale_amount: Decimal
    commission_amount: Decimal

class SaleCreate(SaleBase):
    """
    Request schema for creating a sale.
    """
    pass

class SaleResponse(SaleBase):
    """
    Response schema for returning sale details.
    """
    id: str
    status: SaleStatus
    advance_paid: bool
    reconciled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )