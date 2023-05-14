from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from app.database.database import get_async_session
from app.courier.schemas import CreateCourierRequest, CreateCouriersResponse, CourierDto, GetCouriersResponse
from app.courier.service import add_couriers, get_couriers_all, get_courier_by_id
from app.utils import Paginator, BadRequestResponse, ValidationErrorHandlingRoute, NotFoundResponse

router = APIRouter(
    route_class=ValidationErrorHandlingRoute,
    prefix="/couriers",
    tags=["courier-controller"],
    # dependencies=[Depends(get_async_session)],
    responses={
        400: {
            "description": "bad request",
            "model": BadRequestResponse
        },
        200: {
            "description": "ok"
        }
    }
)


@router.get('', response_model=GetCouriersResponse)
async def get_couriers(pagination_params: Paginator = Depends(), db: AsyncSession = Depends(get_async_session)):
    couriers = await get_couriers_all(pagination_params.limit, pagination_params.offset, db)
    return GetCouriersResponse(couriers=couriers, limit=pagination_params.limit, offset=pagination_params.offset)


@router.get('/{courier_id}', response_model=CourierDto, responses={
    404: {"description": "not found", "model": NotFoundResponse}})
async def get_courier(courier_id: int, db: AsyncSession = Depends(get_async_session)):
    courier = await get_courier_by_id(courier_id, db)
    if not courier:
        raise HTTPException(status_code=404)
    return courier


@router.post('', response_model=CreateCouriersResponse)
async def create_couriers(couriers: CreateCourierRequest, db: AsyncSession = Depends(get_async_session)):
    added_couriers = await add_couriers(couriers.couriers, db)
    return CreateCouriersResponse(couriers=added_couriers)
