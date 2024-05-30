from fastapi import APIRouter, Request, Response, HTTPException, status

from bot_manager import models
from bot_manager.services import AuthServiceDp
from bot_manager.settings import settings


router = APIRouter()


@router.post("/login", response_model=models.Token)
async def login(
    data: models.Login,
    request: Request,
    response: Response,
    auth_service: AuthServiceDp
):
    tokens = await auth_service.login(
        email=data.email,
        password=data.password,
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
