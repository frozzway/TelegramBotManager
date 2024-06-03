from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from bot_manager import models
from bot_manager.services import AuthServiceDp
from bot_manager.settings import settings


router = APIRouter(tags=["Account"])


@router.post("/login", response_model=models.Token)
async def login(
    request: Request,
    response: Response,
    auth_service: AuthServiceDp,
    auth_data: OAuth2PasswordRequestForm = Depends(),
):
    tokens = await auth_service.login(
        email=auth_data.username,
        password=auth_data.password,
        host=request.client.host,
        user_agent=request.headers.get('User-Agent'))

    response.set_cookie(key=settings.jwt_cookie_name, value=tokens.refresh_token)
    return tokens


@router.post("/refresh_token", response_model=models.Token)
async def refresh_token(request: Request, auth_service: AuthServiceDp):
    token = request.cookies.get(settings.jwt_cookie_name)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Cookie with token is missing')

    new_tokens = await auth_service.refresh_token(
        refresh_token=token,
        host=request.client.host,
        user_agent=request.headers.get('User-Agent'))

    return new_tokens
