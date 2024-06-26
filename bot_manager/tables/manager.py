from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from bot_manager.tables import DeclarativeBaseWithId


__all__ = ['ManagerBase', 'Bot', 'User', 'RefreshSession', 'Role']


class ManagerBase(DeclarativeBaseWithId):
    __abstract__ = True


user_role_table = Table(
    "UserRoles",
    ManagerBase.metadata,
    Column("UserId", ForeignKey("Users.id")),
    Column("RoleId", ForeignKey("Roles.id")),
)

user_bot_table = Table(
    "UserBots",
    ManagerBase.metadata,
    Column("UserId", ForeignKey("Users.id")),
    Column("BotId", ForeignKey("Bots.id")),
)


class Bot(ManagerBase):
    __tablename__ = 'Bots'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    database: Mapped[str] = mapped_column()


class User(ManagerBase):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    is_deleted: Mapped[bool] = mapped_column(default=False)

    roles: Mapped[list['Role']] = relationship(secondary=user_role_table, lazy='selectin')
    bots: Mapped[list['Bot']] = relationship(secondary=user_bot_table, lazy='selectin')


class RefreshSession(ManagerBase):
    __tablename__ = 'RefreshSessions'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    token_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    expires_in: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    ip_address: Mapped[str] = mapped_column()
    user_agent: Mapped[str] = mapped_column()


class Role(ManagerBase):
    __tablename__ = 'Roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
