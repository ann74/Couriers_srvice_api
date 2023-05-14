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
