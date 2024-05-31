from typing import Annotated

from fastapi import Depends

from bot_manager.services.auth import AuthService, CurrentUserDp
from bot_manager.services.user_service import UserService


AuthServiceDp = Annotated[AuthService, Depends(AuthService)]
UserServiceDp = Annotated[UserService, Depends(UserService)]
