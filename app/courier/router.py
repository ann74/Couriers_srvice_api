from __future__ import annotations

from datetime import date
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from app.database.database import get_async_session
from app.courier.schemas import CreateCourierRequest, CreateCouriersResponse, CourierDto, GetCouriersResponse,\
    GetCourierMetaInfoResponse
from app.courier.service import add_couriers, get_couriers_all, get_courier_by_id
from app.order.service import get_completed_orders_by_courier_id
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


@router.get('/meta-info/{courier_id}')
async def get_courier_meta_info(courier_id: int, start_date: date, end_date: date,
                                db: AsyncSession = Depends(get_async_session)):
    courier = await get_courier_by_id(courier_id, db)
    courier = jsonable_encoder(courier)
    if not courier:
        raise HTTPException(status_code=404)
    completed_orders = await get_completed_orders_by_courier_id(courier_id, start_date, end_date, db)
    count = len(completed_orders)
    if count == 0:
        return CourierDto(**courier)
    rate = {'FOOT': (2, 3), 'BIKE': (3, 2), 'AUTO': (4, 1)}
    sum_cost = 0
    for order in completed_orders:
        sum_cost += order.cost
    print(sum_cost)
    hours = (end_date - start_date).days * 24
    earnings = sum_cost * rate[courier['courier_type']][0]
    rating = round(count / hours * rate[courier['courier_type']][1])
    courier['earnings'] = earnings
    courier['rating'] = rating
    return GetCourierMetaInfoResponse(**courier)
