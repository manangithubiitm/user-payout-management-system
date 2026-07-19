from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    user_name: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Request schema for creating a new user.
    """
    pass

class UserResponse(UserBase):
    """
    Response schema for returning user details.
    """
    id: str
    wallet_balance: float
    last_withdrawal_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )