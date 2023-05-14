from datetime import datetime

from pydantic import BaseModel, Field, validator


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
    weight: float = Field(gt=0)
    regions: int = Field(gt=0)
    delivery_hours: list[str]
    cost: int = Field(ge=0)

    @validator('delivery_hours')
    def check_delivery_hours(cls, list_hours: list[str]) -> list[str]:
        for hours in list_hours:
            try:
                (h1, m1), (h2, m2) = [map(int, hour.split(':')) for hour in hours.split('-')]
                if not (0 <= h1 <= 23 and 0 <= m1 <= 59 and 0 <= h2 <= 23 and 0 <= m2 <= 59 and
                        (h2 * 60 + m2) > (h1 * 60 + m1)):
                    raise ValueError
            except:
                raise ValueError
        return list_hours




class CreateOrderRequest(BaseModel):
    orders: list[CreateOrderDto]
