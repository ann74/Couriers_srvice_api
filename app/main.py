from app.router import router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        title='Yandex Lavka',
        version='1.0'
    )
    application.include_router(router)

    return application


app = get_application()
