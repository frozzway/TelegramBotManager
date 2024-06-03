from loguru import logger
from sqlalchemy import select, URL
from sqlalchemy.ext.asyncio import create_async_engine

from bot_manager.database import ManagerSessionMaker, url_params
from bot_manager.tables import Bot


engines = {}


async def create_engines():
    async with ManagerSessionMaker() as session:
        result = await session.scalars(select(Bot))
        for bot in result:
            save_engine(bot)


def save_engine(bot: Bot):
    if not engines.get(bot.id):
        url = URL.create('postgresql+asyncpg', database=bot.database, **url_params)
        engines[bot.id] = create_async_engine(url)
        logger.info(f'Created engine for {bot.name} - database: {bot.database}')
