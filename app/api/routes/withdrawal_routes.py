from fastapi import APIRouter, HTTPException, status
from app.models.withdrawal import Withdrawal
from app.schemas.withdrawal import (WithdrawalCreate, WithdrawalResponse)
from app.services.withdrawal_service import WithdrawalService
from app.utils.response_mapper import map_withdrawal_response


router = APIRouter(
    prefix="/withdrawals",
    tags=["Withdrawals"],
)
withdrawal_service = WithdrawalService()

@router.post(
    "",
    response_model=WithdrawalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_withdrawal(withdrawal: WithdrawalCreate):
    try:
        withdrawal_model = Withdrawal(**withdrawal.model_dump())
        withdrawal_id = withdrawal_service.request_withdrawal(withdrawal_model)
        created_withdrawal = (withdrawal_service.get_withdrawal_by_id(withdrawal_id))
        return map_withdrawal_response(created_withdrawal)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.get(
    "/{withdrawal_id}",
    response_model=WithdrawalResponse,
)
def get_withdrawal(withdrawal_id: str):
    try:
        withdrawal = (withdrawal_service.get_withdrawal_by_id(withdrawal_id))
        return map_withdrawal_response(withdrawal)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )