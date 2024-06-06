from fastapi import APIRouter, Response, status

from bot_manager.models import User, UserBase
from bot_manager.roles import Role
from bot_manager.services import UserServiceDp, CurrentUserDp
from bot_manager.services.auth_service import AuthorizeRoles

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/bot", status_code=status.HTTP_204_NO_CONTENT)
async def set_bot(
    bot_id: int,
    response: Response,
    user_service: UserServiceDp,
    current_user: CurrentUserDp
):
    if user_service.has_bot_access(bot_id, current_user):
        response.set_cookie('bot_id', str(bot_id))


@router.post('', response_model=User, dependencies=[AuthorizeRoles(Role.Root)])
async def create_user(data: UserBase, service: UserServiceDp):
    return await service.create(data)
