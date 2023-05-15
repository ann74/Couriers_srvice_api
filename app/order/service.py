from datetime import datetime, date
from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping, update, and_, cast, Date, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order, OrderGroup, GroupOrders
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
    orders = await db.execute(select(Order).order_by(Order.order_id).limit(limit).offset(offset))
    return orders.scalars().all()


async def get_order_group_by_id(id_: int, db: AsyncSession) -> Row | None:
    order_group = await db.execute(select(OrderGroup).where(OrderGroup.order_id == id_))
    return order_group.scalars().first()


async def update_order_info(id_: int, complete_time: datetime, db: AsyncSession) -> None:
    await db.execute(update(OrderGroup).where(OrderGroup.order_id == id_).values(complete=True))
    await db.execute(update(Order).where(Order.order_id == id_).values(completed_time=complete_time))
    await db.commit()


async def get_completed_orders_by_courier_id(id_: int, start_date: date, end_date: date,
                                             db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    row_query = text(f"""SELECT ordr.order_id, ordr.completed_time, gr.courier_id, ordr.cost 
    FROM public.group_orders as gr JOIN public.order_group as og on gr.group_order_id = og.group_order_id
    JOIN public.order as ordr on og.order_id = ordr.order_id
    WHERE gr.courier_id = {id_} and og.complete is TRUE and DATE(ordr.completed_time) >= '{start_date}'
    and DATE(ordr.completed_time) < '{end_date}'""")
    completed_orders = await db.execute(row_query)
    return completed_orders.all()
