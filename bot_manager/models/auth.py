from pydantic import BaseModel, EmailStr, PrivateAttr, ConfigDict

from bot_manager import tables


__all__ = ['UserBase', 'User', 'UserJWT', 'Token', 'Login', 'Role', 'Bot', 'UserCreate']


class Role(BaseModel):
    id: int
    name: str

    _table_class = PrivateAttr(tables.Role)
    model_config = ConfigDict(from_attributes=True)


class Bot(BaseModel):
    id: int
    name: str
    database: str

    _table_class = PrivateAttr(tables.Bot)
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    name: str
    middle_name: str
    surname: str
    roles: list[Role]
    bots: list[Bot]

    _table_class = PrivateAttr(tables.User)


class User(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


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
