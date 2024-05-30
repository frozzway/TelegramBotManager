from sqlalchemy import select

from bot_manager.database import ControllerSession
from bot_manager import models, tables


class UserService:
    def __init__(self, session: ControllerSession):
        self.session = session

    async def get_user(self, user_id) -> tables.User | None:
        stmt = select(tables.User).where(tables.User.id == user_id)
        return await self.session.scalar(stmt)

