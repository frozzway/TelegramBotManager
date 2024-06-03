from fastapi import APIRouter, HTTPException, status

from bot_manager.models import CategoryBase, Category
from bot_manager.services import CategoryServiceDp


router = APIRouter(prefix='/category', tags=['Categories'])


@router.post("/", response_model=Category)
async def create_category(data: CategoryBase, service: CategoryServiceDp):
    return await service.create(data)


@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int, service: CategoryServiceDp):
    return await service.get(category_id)


@router.delete("/{category_id}", response_model=Category)
async def delete_category(category_id: int, service: CategoryServiceDp):
    if category_id == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Нельзя удалить главную категорию")
    return await service.delete(category_id)


@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, data: CategoryBase, service: CategoryServiceDp):
    return await service.update(category_id, data)


@router.get('/', response_model=list[Category])
async def get_all_categories(service: CategoryServiceDp):
    return await service.get_all()
