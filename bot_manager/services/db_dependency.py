from typing import Annotated
from typing import AsyncGenerator

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from bot_manager.services.auth_service import CurrentUserDp
from bot_manager.engines import engines


BotId = Annotated[int | None, Cookie()]


async def get_bot_session(bot_id: BotId, current_user: CurrentUserDp) -> AsyncGenerator[AsyncSession, None]:
    if bot_id not in current_user.bots_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    engine = engines[bot_id]
    session = AsyncSession(bind=engine, expire_on_commit=False)
    await session.begin()
    try:
        yield session
    finally:
        await session.close()


BotSession = Annotated[AsyncSession, Depends(get_bot_session)]
