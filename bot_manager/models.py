from pydantic import BaseModel, ConfigDict, EmailStr

from bot_manager.roles import Role


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
    roles: list[Role]


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Login(BaseModel):
    email: EmailStr
    password: str
