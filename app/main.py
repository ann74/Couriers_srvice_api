from app.order.router import router as order_router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        title='Yandex Lavka',
        version='1.0'
    )
    application.include_router(order_router)

    return application


app = get_application()
