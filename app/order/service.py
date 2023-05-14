from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order
from app.order.schemas import CreateOrderDto, OrderDto


async def add_orders(orders: list[CreateOrderDto], db: AsyncSession) -> list[OrderDto]:
    new_orders = [Order(**order.dict()) for order in orders]
    db.add_all(new_orders)
    await db.commit()
    return new_orders


async def get_order_by_id(id_: int, db: AsyncSession) -> OrderDto | None:
    order = await db.get(Order, id_)
    return order


async def get_orders_all(limit: int, offset: int, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    orders = await db.execute(select(Order).limit(limit).offset(offset))
    return orders.scalars().all()
