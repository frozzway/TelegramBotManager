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


@router.post('/', dependencies=[AuthorizeRoles(Role.Root)], response_model=User)
async def create_user(data: UserBase, service: UserServiceDp):
    return await service.create(data)


@router.delete('/{user_id}', dependencies=[AuthorizeRoles(Role.Root)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDp):
    return await service.delete(user_id)


@router.put('/{user_id}', dependencies=[AuthorizeRoles(Role.Root)], response_model=User)
async def update_user(user_id: int, data: UserBase, service: UserServiceDp):
    return await service.update(user_id, data)


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, service: UserServiceDp):
    return await service.get(user_id)


@router.get('/', dependencies=[AuthorizeRoles(Role.Root)], response_model=list[User])
async def get_all_users(service: UserServiceDp):
    return await service.get_all()
