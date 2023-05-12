from typing import AsyncGenerator
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import DB_URL


DATABASE_URL = DB_URL
Base = declarative_base()


engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, future=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Paginator:
    def __init__(self, limit: int = 1, offset: int = 0):
        if limit < 1 or offset < 0:
            raise HTTPException(status_code=400)
        self.limit = limit
        self.offset = offset
