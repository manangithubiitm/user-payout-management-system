from fastapi import APIRouter, HTTPException, status
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale_service import SaleService
from app.utils.response_mapper import map_sale_response

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)
sale_service = SaleService()

# Create sale
@router.post(
    "",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sale(sale: SaleCreate):
    try:
        sale_model = Sale(**sale.model_dump())
        sale_id = sale_service.create_sale(sale_model)
        created_sale = sale_service.get_sale_by_id(sale_id)
        return map_sale_response(created_sale)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
def get_sale(sale_id: str):
    try:
        sale = sale_service.get_sale_by_id(sale_id)
        return map_sale_response(sale)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/{sale_id}/approve",
    status_code=status.HTTP_200_OK,
)
def approve_sale(sale_id: str):
    try:
        sale_service.approve_sale(sale_id)
        updated_sale = sale_service.get_sale_by_id(sale_id)
        return map_sale_response(updated_sale)
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

@router.post(
    "/{sale_id}/reject",
    status_code=status.HTTP_200_OK,
)
def reject_sale(sale_id: str):
    try:
        sale_service.reject_sale(sale_id)
        updated_sale = sale_service.get_sale_by_id(sale_id)
        return map_sale_response(updated_sale)
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