from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot_manager.settings import settings


url_params = {
    'username': settings.db_username,
    'password': settings.db_password,
    'host': settings.db_host,
    'port': settings.db_port,
}

async_url_object = URL.create(
    'postgresql+asyncpg',
    database=settings.db_database,
    **url_params
)

async_engine = create_async_engine(async_url_object, pool_size=5, max_overflow=0, pool_timeout=3600)
ManagerSessionMaker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_manager_session() -> AsyncGenerator[AsyncSession, None]:
    session = ManagerSessionMaker()
    await session.begin()
    try:
        yield session
    finally:
        await session.close()

ManagerSession = Annotated[AsyncSession, Depends(get_manager_session)]