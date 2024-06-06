from typing import Annotated

from fastapi import Depends

from bot_manager.services.elements_services import LinkButtonService, CategoryService, ScenarioService
from bot_manager.services.ownership_service import OwnershipService
from bot_manager.services.auth_service import AuthService, CurrentUserDp
from bot_manager.services.user_service import UserService
from bot_manager.services.email_service import EmailService


AuthServiceDp = Annotated[AuthService, Depends(AuthService)]
UserServiceDp = Annotated[UserService, Depends(UserService)]
CategoryServiceDp = Annotated[CategoryService, Depends(CategoryService)]
LinkButtonServiceDp = Annotated[LinkButtonService, Depends(LinkButtonService)]
ScenarioServiceDp = Annotated[ScenarioService, Depends(ScenarioService)]
OwnershipServiceDp = Annotated[OwnershipService, Depends(OwnershipService)]
