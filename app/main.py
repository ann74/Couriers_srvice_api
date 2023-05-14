from typing import Any

from fastapi import FastAPI

from app.order.router import router as order_router


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

    return application


app = get_application()
