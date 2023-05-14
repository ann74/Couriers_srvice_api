from fastapi import Response, Request
from fastapi.exceptions import RequestValidationError
from typing import Callable
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel


class Paginator:
    def __init__(self, limit: int = 1, offset: int = 0):
        if limit < 0 or offset < 0:
            raise HTTPException(status_code=400, detail='Validation Failed')
        self.limit = limit
        self.offset = offset


class BadRequestResponse(BaseModel):
    ...


class NotFoundResponse(BaseModel):
    ...


class ValidationErrorHandlingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError:
                raise HTTPException(status_code=400, detail='Validation Failed')

        return custom_route_handler


def validate_hours(cls, list_hours: list[str]) -> list[str]:
    for hours in list_hours:
        try:
            (h1, m1), (h2, m2) = [map(int, hour.split(':')) for hour in hours.split('-')]
            if not (0 <= h1 <= 23 and 0 <= m1 <= 59 and 0 <= h2 <= 23 and 0 <= m2 <= 59 and
                    (h2 * 60 + m2) > (h1 * 60 + m1)):
                raise ValueError
        except:
            raise ValueError
    return list_hours
