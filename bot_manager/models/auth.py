from pydantic import BaseModel, ConfigDict, EmailStr

from bot_manager.roles import Role


__all__ = ['UserCreate', 'User', 'UserJWT', 'Token', 'Login']


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    middle_name: str
    surname: str
    roles: list[Role]


class User(UserCreate):
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
