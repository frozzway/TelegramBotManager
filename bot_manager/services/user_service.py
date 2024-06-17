import secrets

from fastapi import HTTPException, status
from sqlalchemy import select

from bot_manager.database import ManagerSession
from bot_manager.models import UserJWT, UserBase, UserCreate
from bot_manager.services import AuthService, EmailService, CurrentUserDp
from bot_manager.services.crud_service import CrudService, CRUDServiceExtended, CRUDConfiguration
from bot_manager.roles import Role as RoleEnum
from bot_manager import tables


class UserService(CrudService):
    def __init__(self, session: ManagerSession, current_user: CurrentUserDp):
        super().__init__(session, tables.User)
        self.current_user = current_user
        self.crud_service = CRUDServiceExtended(session)

    @staticmethod
    def has_bot_access(bot_id: int, current_user: UserJWT) -> bool:
        if bot_id not in current_user.bots_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return True

    async def create_roles(self):
        for role in RoleEnum:
            if not await self.session.scalar(select(tables.Role).where(tables.Role.name == role.value)):
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
            roles=[root_role]
        )
        self.session.add(admin)
        await self.session.commit()

    async def create(self, model: UserCreate) -> tables.User:
        """Создать пользователя и отправить данные для входа на его email"""
        config = CRUDConfiguration(allow_sub_create=False, allow_update=False)
        self.crud_service.config = config
        password = model.password
        model = UserBase.model_construct(**model.model_dump())
        user = await self.crud_service.create(model, subsequent_call=False)
        user.hashed_password = AuthService.hash_string(password)
        self.session.add(user)
        await self.session.flush()
        # await EmailService.send_registration_email(model.email, password)
        await self.session.commit()
        return user

    async def update(self, entity_id: int, model: UserBase) -> tables.User:
        config = CRUDConfiguration(allow_sub_create=False, allow_update=False)
        self.crud_service.config = config

        user = await self.get(entity_id)
        user = await self.crud_service.update(model, user, subsequent_call=False)
        await self.session.commit()
        return user

    async def delete(self, entity_id: int) -> None:
        user: tables.User = await self.get(entity_id)
        user.is_deleted = True
        await self.session.commit()

    async def get(self, entity_id: int) -> tables.User:
        root_access = RoleEnum.Root in [RoleEnum(r) for r in self.current_user.roles]
        if self.current_user.id == entity_id or root_access:
            return await super().get(entity_id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
