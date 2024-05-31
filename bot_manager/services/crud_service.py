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
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Table]:
        stmt = select(self.table)
        return list(await self.session.scalars(stmt))

    async def create(self, model: BaseModel) -> Table:
        entity = self.table(**model.model_dump())
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def update(self, model: Model) -> Table:
        entity = await self.get(model.id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        for field in model.model_fields_set:
            setattr(entity, field, getattr(model, field))
        await self.session.commit()
        return entity

    async def delete(self, entity_id: int) -> None:
        stmt = delete(self.table).where(self.table.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()
