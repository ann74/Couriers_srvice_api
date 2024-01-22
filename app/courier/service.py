from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.courier.models import Courier
from app.courier.schemas import CourierDto, CreateCourierDto


async def add_couriers(couriers: list[CreateCourierDto], db: AsyncSession) -> list[CourierDto]:
    new_couriers = [Courier(**courier.dict()) for courier in couriers]
    db.add_all(new_couriers)
    await db.commit()
    return new_couriers


async def get_courier_by_id(id_: int, db: AsyncSession) -> CourierDto | None:
    courier = await db.get(Courier, id_)
    return courier


async def get_couriers_all(limit: int, offset: int, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    couriers = await db.execute(select(Courier).order_by(Courier.courier_id).limit(limit).offset(offset))
    return couriers.unique().scalars().all()
