from datetime import datetime

from pydantic import BaseModel


class OrderDto(BaseModel):
    order_id: int
    weight: float
    regions: int
    delivery_hours: list[str]
    cost: int
    completed_time: datetime | None

    class Config:
        orm_mode = True


class CreateOrderDto(BaseModel):
    weight: float
    regions: int
    delivery_hours: list[str]
    cost: int


class CreateOrderRequest(BaseModel):
    orders: list[CreateOrderDto]
