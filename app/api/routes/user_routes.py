from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.user_service import UserService
from app.utils.response_mapper import map_user_response

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
user_service = UserService()

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate):
    # Converts the validated request into your domain model
    try:
        user_model = User(
            **user.model_dump()
        )
        user_id = user_service.create_user(user_model)
        created_user = user_service.get_user_by_id(user_id)
        return map_user_response(created_user)
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
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(user_id: str):
    try:
        user = user_service.get_user_by_id(user_id)
        return map_user_response(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )