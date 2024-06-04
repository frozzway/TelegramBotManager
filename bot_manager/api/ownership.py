from fastapi import APIRouter, status

from bot_manager.models import Ownership, Category
from bot_manager.services import OwnershipServiceDp


router = APIRouter(prefix='/ownership', tags=['Ownership'])


@router.get('/category/{parent_id}', response_model=list[Category])
async def get_available_child_categories(parent_id: int, service: OwnershipServiceDp):
    return await service.get_available_categories(parent_id)


@router.post('/{parent_id}', status_code=status.HTTP_201_CREATED)
async def set_ownership(parent_id: int, data: list[list[Ownership]], service: OwnershipServiceDp):
    await service.set_ownership(parent_id, data)
