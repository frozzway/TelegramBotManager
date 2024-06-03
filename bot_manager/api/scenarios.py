from fastapi import APIRouter

from bot_manager.models import ScenarioButton
from bot_manager.services import ScenarioServiceDp


router = APIRouter(prefix='/scenario', tags=['Scenarios'])


@router.get('/', response_model=list[ScenarioButton])
async def get_all(service: ScenarioServiceDp):
    return await service.get_all()
