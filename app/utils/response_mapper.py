from app.schemas.user import UserResponse
from app.schemas.sale import SaleResponse
from app.schemas.withdrawal import WithdrawalResponse

def map_user_response(user: dict) -> UserResponse:
    return UserResponse(
        id=user["_id"],
        user_name=user["user_name"],
        email=user["email"],
        wallet_balance=user["wallet_balance"],
        last_withdrawal_at=user["last_withdrawal_at"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )

def map_sale_response(sale: dict) -> SaleResponse:
    return SaleResponse(
        id=sale["_id"],
        user_id=sale["user_id"],
        brand_name=sale["brand_name"],
        sale_amount=sale["sale_amount"],
        commission_amount=sale["commission_amount"],
        status=sale["status"],
        advance_paid=sale["advance_paid"],
        reconciled=sale["reconciled"],
        created_at=sale["created_at"],
        updated_at=sale["updated_at"],
    )

def map_withdrawal_response(withdrawal: dict) -> WithdrawalResponse:
    return WithdrawalResponse(
        id=withdrawal["_id"],
        user_id=withdrawal["user_id"],
        amount=withdrawal["amount"],
        status=withdrawal["status"],
        recovered=withdrawal.get("recovered", False),
        requested_at=withdrawal["requested_at"],
        processed_at=withdrawal["processed_at"],
        created_at=withdrawal["created_at"],
        updated_at=withdrawal["updated_at"],
    )