from pydantic import BaseModel, EmailStr

from bot_manager.roles import Role


__all__ = ['UserBase', 'User', 'UserJWT', 'Token', 'Login']


class UserBase(BaseModel):
    email: EmailStr
    name: str
    middle_name: str
    surname: str
    roles: list[Role]


class User(UserBase):
    id: int


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
