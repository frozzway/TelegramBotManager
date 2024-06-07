from contextlib import asynccontextmanager

from alembic import command
from fastapi import FastAPI

from bot_manager.api import router as api_router
from bot_manager.database import get_manager_session
from bot_manager.engines import create_engines
from bot_manager.services import UserService
from bot_manager.settings import alembic_cfg


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл"""
    await create_engines()
    session_maker = app.dependency_overrides.get(get_manager_session, get_manager_session)()
    session = await anext(session_maker)
    user_service = UserService(session, None)
    await user_service.create_roles()
    await user_service.create_admin_account()
    yield


def run_migrations():
    command.upgrade(config=alembic_cfg, revision='head')


run_migrations()

app = FastAPI(title='Сервис управления содержанием Telegram ботов', lifespan=lifespan)
app.router.include_router(api_router)
