from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot_manager.engines import create_engines
from bot_manager.database import async_engine
from bot_manager.tables import ManagerBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл микросервиса"""
    await create_tables()
    await create_engines()
    yield


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(ManagerBase.metadata.create_all)


app = FastAPI(title='Сервис по взаимодействию с ArmGS', lifespan=lifespan)