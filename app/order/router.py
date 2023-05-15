from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from app.database.database import get_async_session
from app.order.schemas import CreateOrderRequest, OrderDto, CompleteOrderRequestDto
from app.order.service import add_orders, get_order_by_id, get_orders_all, get_order_group_by_id, update_order_info
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


@router.post('/complete', response_model=list[OrderDto])
async def complete_orders(orders: CompleteOrderRequestDto, db: AsyncSession = Depends(get_async_session)):
    completed_orders = []
    for order in orders.complete_info:
        order_courier = await get_order_group_by_id(order.order_id, db)
        if not order_courier:
            # print(f'нет заказа в назначенных {order.order_id}')
            raise HTTPException(status_code=400)
        if order_courier.group_orders.courier_id != order.courier_id:
            # print(f'назначен курьер {order_courier.group_orders.courier_id}, а запрашивается {order.courier_id}')
            raise HTTPException(status_code=400)
        if not order_courier.complete:
            await update_order_info(order.order_id, order.complete_time, db)
        completed_orders.append(order_courier.order)
    return completed_orders
