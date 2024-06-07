from typing import Any, Iterable
from pydantic import BaseModel, EmailStr, field_validator

from bot_manager.roles import Role
from bot_manager import tables


__all__ = ['UserBase', 'User', 'UserJWT', 'Token', 'Login']


class UserBase(BaseModel):
    email: EmailStr
    name: str
    middle_name: str
    surname: str
    roles: list[Role]


class User(UserBase):
    id: int

    # noinspection PyNestedDecorators
    @field_validator('roles', mode='before')
    @classmethod
    def modify_role_types(cls, raw_value: Any):
        result = []
        if isinstance(raw_value, Iterable):
            for role_entity in raw_value:
                item = Role(role_entity.name) if isinstance(role_entity, tables.Role) else role_entity
                result.append(item)
            return result
        return raw_value


class UserJWT(BaseModel):
    id: int
    roles: list[str]
    bots_id: list[int]


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Login(BaseModel):
    username: EmailStr
    password: str
