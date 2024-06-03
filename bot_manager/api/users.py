from fastapi import APIRouter, Response, status

from bot_manager.services import UserServiceDp, CurrentUserDp

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
