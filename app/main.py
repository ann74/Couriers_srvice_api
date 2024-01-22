from typing import Any

from fastapi import FastAPI

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.order.router import router as order_router
from app.courier.router import router as courier_router


limiter = Limiter(key_func=get_remote_address, application_limits=["10/second"], key_style="endpoint")


class CustomFastApi(FastAPI):
    def openapi(self) -> dict[str, Any]:
        super().openapi()
        for _, method_item in self.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']
        schemas = self.openapi_schema.get('components').get('schemas')
        if 'HTTPValidationError' in schemas:
            del schemas['HTTPValidationError']
        if 'ValidationError' in schemas:
            del schemas['ValidationError']
        return self.openapi_schema


def get_application() -> FastAPI:
    application = CustomFastApi(
        title='Yandex Lavka',
        version='1.0'
    )
    application.include_router(order_router)
    application.include_router(courier_router)
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(SlowAPIMiddleware)

    return application


app = get_application()
