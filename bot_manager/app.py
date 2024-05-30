from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot_manager.engines import create_engines


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл микросервиса"""
    await create_engines()
    yield


app = FastAPI(title='Сервис по взаимодействию с ArmGS', lifespan=lifespan)