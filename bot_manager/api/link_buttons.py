from fastapi import APIRouter, status

from bot_manager.models import LinkButton, LinkButtonBase
from bot_manager.services import LinkButtonServiceDp


router = APIRouter(prefix='/link_button', tags=['LinkButtons'])


@router.post("/", response_model=LinkButton)
async def create_link_button(data: LinkButtonBase, service: LinkButtonServiceDp):
    return await service.create(data)


@router.get("/{link_button_id}", response_model=LinkButton)
async def get_link_button(link_button_id: int, service: LinkButtonServiceDp):
    return await service.get(link_button_id)


@router.delete("/{link_button_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link_button(link_button_id: int, service: LinkButtonServiceDp):
    await service.delete(link_button_id)


@router.put("/{link_button_id}", response_model=LinkButton)
async def update_link_button(link_button_id: int, data: LinkButtonBase, service: LinkButtonServiceDp):
    return await service.update(link_button_id, data)


@router.get('/', response_model=list[LinkButton])
async def get_all_link_buttons(service: LinkButtonServiceDp):
    return await service.get_all()
