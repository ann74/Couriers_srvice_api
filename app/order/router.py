from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from app.database.database import get_async_session
from app.order.schemas import CreateOrderRequest, OrderDto
from app.order.service import add_orders, get_order_by_id, get_orders_all
from app.utils import Paginator, BadRequestResponse, ValidationErrorHandlingRoute, NotFoundResponse

router = APIRouter(
    route_class=ValidationErrorHandlingRoute,
    prefix="/orders",
    tags=["order-controller"],
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


@router.get('', response_model=list[OrderDto])
async def get_orders(pagination_params: Paginator = Depends(), db: AsyncSession = Depends(get_async_session)):
    return await get_orders_all(pagination_params.limit, pagination_params.offset, db)


@router.get('/{order_id}', response_model=OrderDto, responses={
    404: {"description": "not found", "model": NotFoundResponse}})
async def get_order(order_id: int, db: AsyncSession = Depends(get_async_session)):
    order = await get_order_by_id(order_id, db)
    if not order:
        raise HTTPException(status_code=404)
    return order


@router.post('', response_model=list[OrderDto])
async def create_orders(orders: CreateOrderRequest, db: AsyncSession = Depends(get_async_session)):
    return await add_orders(orders.orders, db)
