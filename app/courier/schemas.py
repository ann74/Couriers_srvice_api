from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, validator
from pydantic.types import PositiveInt

from app.utils import validate_hours


class CourierType(str, Enum):
    """
        Тип курьера - пешеход, на велосипеде или на автомобиле
    """
    foot = "FOOT"
    bike = "BIKE"
    auto = "AUTO"


class CourierDto(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: list[int]
    working_hours: list[str]

    class Config:
        orm_mode = True


class CreateCourierDto(BaseModel):
    courier_type: CourierType
    regions: list[PositiveInt]
    working_hours: list[str]

    _validate_hours = validator('working_hours', allow_reuse=True)(validate_hours)


class CreateCourierRequest(BaseModel):
    couriers: list[CreateCourierDto]


class CreateCouriersResponse(BaseModel):
    couriers: list[CourierDto]


class GetCouriersResponse(BaseModel):
    couriers: list[CourierDto]
    limit: int
    offset: int


class GetCourierMetaInfoResponse(CourierDto):
    rating: int = 0
    earnings: int = 0
