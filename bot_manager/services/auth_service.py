from datetime import datetime, timedelta
from typing import Annotated
import secrets

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
import bcrypt
from pydantic import ValidationError
from sqlalchemy import select, delete

from bot_manager import models, tables
from bot_manager.settings import settings
from bot_manager.database import ManagerSession
from bot_manager.roles import Role as RoleEnum
from bot_manager.tables import RefreshSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.UserJWT:
    return AuthService.verify_token(token)


CurrentUserDp = Annotated[models.UserJWT, Depends(get_current_user)]


class AuthorizeRoles:
    @staticmethod
    def construct_callable(*roles: RoleEnum):
        def func(current_user: CurrentUserDp):
            for role in current_user.roles:
                if RoleEnum(role) in roles:
                    return True
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return func

    def __new__(cls, *roles: RoleEnum):
        callable_obj = AuthorizeRoles.construct_callable(*roles)
        return Depends(callable_obj)


class AuthService:
    def __init__(self, session: ManagerSession):
        self.session = session

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

    @staticmethod
    def hash_string(data: str) -> str:
        pwd_bytes = data.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_token(token: str) -> models.UserJWT:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = models.UserJWT.model_validate(user_data)
        except ValidationError:
            raise exception from None

        return user

    @staticmethod
    def create_tokens(user: tables.User) -> models.Token:
        user_data = models.UserJWT(
            id=user.id,
            roles=[r.name for r in user.roles],
            bots_id=[b.id for b in user.bots],
        )
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.id),
            'user': user_data.model_dump(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return models.Token(access_token=token, refresh_token=secrets.token_hex(32))

    async def get_refresh_session(self, hashed_token: str) -> RefreshSession:
        return await self.session.scalar(
            select(RefreshSession)
            .where(
                RefreshSession.token_hash == hashed_token,
                RefreshSession.expires_in <= datetime.utcnow()))

    async def _remove_expired_sessions(self, user_id: int) -> None:
        await self.session.execute(
            delete(RefreshSession)
            .where(
                RefreshSession.user_id == user_id,
                RefreshSession.expires_in > datetime.utcnow()))

    async def _create_refresh_session(self, refresh_token: str, user_id: int, host: str, user_agent: str) -> RefreshSession:
        refresh_session = RefreshSession(
            user_id=user_id,
            token_hash=self.hash_string(refresh_token),
            created_at=datetime.utcnow(),
            expires_in=datetime.utcnow() + timedelta(seconds=settings.jwt_refresh_token_expires_s),
            ip_address=host,
            user_agent=user_agent
        )
        self.session.add(refresh_session)
        return refresh_session

    async def refresh_token(self, refresh_token: str, host: str, user_agent: str) -> models.Token:
        hashed_token = self.hash_string(refresh_token)
        refresh_session = await self.get_refresh_session(hashed_token)
        if not refresh_session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired or invalid')
        user_id = refresh_session.user_id
        await self._remove_expired_sessions(user_id)
        user = await self.session.scalar(select(tables.User).where(tables.User.id == user_id, tables.User.is_deleted.is_(False)))
        new_tokens = self.create_tokens(user)
        await self._create_refresh_session(new_tokens.refresh_token, user_id, host, user_agent)
        await self.session.commit()
        return new_tokens

    async def login(self, email: str, password: str, host: str, user_agent: str) -> models.Token:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        user = await self.session.scalar(select(tables.User).where(tables.User.email == email, tables.User.is_deleted.is_(False)))
        if not user or not self.verify_password(password, user.hashed_password):
            raise exception
        tokens = self.create_tokens(user)
        await self._create_refresh_session(tokens.refresh_token, user.id, host, user_agent)
        await self.session.commit()
        return tokens
