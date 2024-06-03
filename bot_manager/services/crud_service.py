from typing import TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot_manager import models, tables


Table = TypeVar('Table', bound=tables.DeclarativeBase)
Model = TypeVar('Model', bound=models.BaseModelWithId)


class CrudService:
    def __init__(self, session: AsyncSession, table: type[Table]):
        self.session = session
        self.table = table

    async def get(self, entity_id: int) -> Table:
        stmt = select(self.table).where(self.table.id == entity_id)
        entity = await self.session.scalar(stmt)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return entity

    async def get_all(self) -> list[Table]:
        stmt = select(self.table)
        return list(await self.session.scalars(stmt))

    async def create(self, model: BaseModel) -> Table:
        entity = self.table(**model.model_dump())
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def update(self, entity_id: int, model: Model) -> Table:
        entity = await self.get(entity_id)
        dumped_model = model.model_dump()
        for field in dumped_model.keys():
            new_value = dumped_model.get(field)
            setattr(entity, field, new_value)
        await self.session.commit()
        return entity

    async def delete(self, entity_id: int) -> None:
        await self.get(entity_id)
        stmt = delete(self.table).where(self.table.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()
