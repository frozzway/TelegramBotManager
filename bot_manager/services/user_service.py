import secrets

from fastapi import HTTPException, status
from sqlalchemy import select

from bot_manager.database import ManagerSession
from bot_manager.models import UserJWT, UserBase
from bot_manager.services import AuthService, EmailService
from bot_manager.services.crud_service import CrudService
from bot_manager.roles import Role
from bot_manager import tables


class UserService(CrudService):
    def __init__(self, session: ManagerSession):
        super().__init__(session, tables.User)

    @staticmethod
    def has_bot_access(bot_id: int, current_user: UserJWT) -> bool:
        if bot_id not in current_user.bots_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return True

    async def create_roles(self):
        for role in Role:
            if not await self.session.scalar(select(tables.Role).where(tables.Role.name == role.name)):
                entity = tables.Role(name=role.value)
                self.session.add(entity)
        await self.session.commit()

    async def create_admin_account(self):
        password_hash = AuthService.hash_string('qwerty123!')
        root_role = await self.session.scalar(select(tables.Role).where(tables.Role.name == 'root'))
        admin = await self.session.scalar(select(tables.User).where(tables.User.id == 1))
        if admin:
            return
        admin = tables.User(
            id=1,
            name='Admin',
            middle_name='Admin',
            surname='Admin',
            email='administrator@localhost.ru',
            hashed_password=password_hash,
            roles={root_role}
        )
        self.session.add(admin)
        await self.session.commit()

    async def create(self, model: UserBase) -> tables.User:
        """Создать пользователя и отправить данные для входа на его email"""
        user = tables.User(**model.model_dump())
        password = secrets.token_urlsafe(12)
        user.hashed_password = AuthService.hash_string(password)
        async with self.session.begin():
            self.session.add(user)
            await self.session.flush()
            await EmailService.send_registration_email(model.email, password)
            await self.session.commit()
        return user
