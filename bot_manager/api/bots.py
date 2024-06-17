from fastapi import APIRouter

from bot_manager.models import Bot, BaseBot
from bot_manager.roles import Role
from bot_manager.services import BotServiceDp
from bot_manager.services.auth_service import AuthorizeRoles

router = APIRouter(prefix='/bots', tags=['Bots'], dependencies=[AuthorizeRoles(Role.Root)])


@router.post("/", response_model=Bot)
async def create_bot(data: BaseBot, service: BotServiceDp):
    return await service.create(data)


@router.get('/', response_model=list[Bot])
async def get_all_bots(service: BotServiceDp):
    return await service.get_all()
