from fastapi import APIRouter
from app.api.routes.user_routes import router as user_router
from app.api.routes.sale_routes import router as sale_router
from app.api.routes.withdrawal_routes import router as withdrawal_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(sale_router)
api_router.include_router(withdrawal_router)