from datetime import datetime
from typing import Union

from sqlalchemy import ForeignKey, Table, Column, TIMESTAMP
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship

from bot_manager.roles import Role as RoleEnum


class AiogramBase(DeclarativeBase):
    pass


class ControllerBase(DeclarativeBase):
    pass


class Category(AiogramBase):
    """Категория"""
    __tablename__ = 'Categories'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(comment='Наименование категории (заголовок)')
    text: Mapped[str | None] = mapped_column(comment='Текст категории')
    tree_header: Mapped[bool] = mapped_column(default=False, comment='Флаг вывода наименования категории с наименованием родителя')
    page_size: Mapped[int | None] = mapped_column(comment='Количество кнопок на одной странице категории (при пагинации)')


class Button(AiogramBase):
    """Базовый класс для всех элементов, не являющимися категориями"""
    __tablename__ = "Buttons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    Discriminator: Mapped[str]

    __mapper_args__ = {
        "polymorphic_abstract": True,
        "polymorphic_on": "Discriminator",
    }


class LinkButton(Button):
    """Кнопка-ссылка на url"""
    url: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "LinkButton",
    }


class ScenarioButton(Button):
    """Кнопка вызывающая сценарий"""
    callback_url: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "ScenarioButton",
    }

    def __hash__(self):
        return hash(self.callback_url)

    def __eq__(self, other):
        return isinstance(other, ScenarioButton) and self.callback_url == other.callback_url


class Ownership(AiogramBase):
    """Принадлежность категорий и элементов родительской категории"""
    __tablename__ = 'Ownerships'
    id: Mapped[int] = mapped_column(primary_key=True)

    owner_category_id: Mapped[int] = mapped_column(ForeignKey('Categories.id'), comment='Категория, к которой отнесен элемент')
    category_id: Mapped[int | None] = mapped_column(ForeignKey('Categories.id'), comment='Отнесенная категория')
    button_id: Mapped[int | None] = mapped_column(ForeignKey('Buttons.id'), comment='Отнесенный элемент')
    position_x: Mapped[int | None] = mapped_column(comment='Позиция элемента в категории (номер столбца)')
    position_y: Mapped[int] = mapped_column(comment='Позиция элемента в категории (номер строки)')


Element = Union[Category, LinkButton, ScenarioButton]


class Bot(ControllerBase):
    __tablename__ = 'Bots'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    database: Mapped[str] = mapped_column()


user_role_table = Table(
    "UserRoles",
    ControllerBase.metadata,
    Column("UserId", ForeignKey("Users.id")),
    Column("RoleId", ForeignKey("Roles.id")),
)


class User(ControllerBase):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    roles: Mapped[set['Role']] = relationship(secondary=user_role_table, lazy='selectin')


class RefreshSession(ControllerBase):
    __tablename__ = 'RefreshSessions'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    token_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    expires_in: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    ip_address: Mapped[str] = mapped_column()
    user_agent: Mapped[str] = mapped_column()


class Role(ControllerBase):
    __tablename__ = 'Roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        table = isinstance(other, Role) and self.name == other.name
        enum = isinstance(other, RoleEnum) and self.name == other.value
        return table or enum
