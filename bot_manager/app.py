from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot_manager.api import router as api_router
from bot_manager.database import async_engine, get_manager_session
from bot_manager.engines import create_engines
from bot_manager.services import UserService
from bot_manager.tables import ManagerBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл микросервиса"""
    await create_tables()
    await create_engines()
    session_maker = app.dependency_overrides.get(get_manager_session, get_manager_session)()
    session = await anext(session_maker)
    user_service = UserService(session)
    await user_service.create_roles()
    await user_service.create_admin_account()
    yield


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(ManagerBase.metadata.create_all)


app = FastAPI(title='Сервис по взаимодействию с ArmGS', lifespan=lifespan)
app.router.include_router(api_router)
