from fastapi import APIRouter

router = APIRouter(
    prefix="/withdrawals",
    tags=["Withdrawals"],
)