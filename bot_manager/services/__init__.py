from typing import Annotated

from fastapi import Depends

from bot_manager.services.auth import AuthService
from bot_manager.services.user_service import UserService


UserServiceDp = Annotated[UserService, Depends(UserService)]
AuthServiceDp = Annotated[AuthService, Depends(AuthService)]
