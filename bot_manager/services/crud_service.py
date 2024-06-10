from dataclasses import dataclass
from typing import TypeVar, Iterable, Collection

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot_manager import tables


Table = TypeVar('Table', bound=tables.DeclarativeBaseWithId)
SUPPORTED_ITERABLES = (list, tuple, set)


@dataclass
class CRUDConfiguration:
    delete_old_values: bool = False
    allow_sub_create: bool = True
    allow_update: bool = True


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

    async def update(self, entity_id: int, model: BaseModel) -> Table:
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


class CRUDServiceExtended:
    def __init__(self, session: AsyncSession, config: CRUDConfiguration = None):
        self.session = session
        if config is None:
            config = CRUDConfiguration()
        self.config = config

    async def create(self, model: BaseModel, subsequent_call: bool = True) -> Table:
        if not self.config.allow_sub_create and subsequent_call:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'Creation of entities {model._table_class} is not allowed')
        current_level_fields = {}
        for field_name in model.model_fields.keys():
            value = getattr(model, field_name)
            if isinstance(value, BaseModel):
                current_level_fields[field_name] = await self.to_orm(value)
            elif isinstance(value, SUPPORTED_ITERABLES):
                mapped_orm_entities = await self.map_collection(value)
                current_level_fields[field_name] = mapped_orm_entities
            else:
                current_level_fields[field_name] = value

        return model._table_class(**current_level_fields)

    async def to_orm(self, model: BaseModel) -> Table:
        if not hasattr(model, 'id'):
            return await self.create(model)
        else:
            entity = await self.get(model._table_class, model.id)
            return await self.update(model, entity)

    async def update_many(self, model_collection: Iterable[BaseModel], table: type[Table]) -> list[Table]:
        model_collection = sorted(model_collection, key=lambda m: m.id)
        entities_ids = {m.id for m in model_collection}
        entities = await self.session.scalars(select(table).where(table.id.in_(entities_ids)).order_by(table.id))
        entities = list(entities)
        existing_entities_id: set[int] = {e.id for e in entities}
        if non_existing_ids := entities_ids - existing_entities_id:
            non_existing_ids_s = ','.join((str(i) for i in non_existing_ids))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Objects of type {table} with id {non_existing_ids_s} not found')
        return [await self.update(model, entity) for model, entity in zip(model_collection, entities)]

    async def map_collection(self, collection: Iterable[BaseModel]) -> list[Table]:
        collection = list(collection)
        if len(collection) == 0:
            return []

        mapped_orm_entities = []
        table = collection[0]._table_class
        existing = [model for model in collection if hasattr(model, 'id')]
        new = [model for model in collection if not hasattr(model, 'id')]
        mapped_orm_entities.extend(await self.update_many(existing, table))
        mapped_orm_entities.extend([await self.create(model) for model in new])
        return mapped_orm_entities

    async def update(self, model: BaseModel, table_entity: Table, subsequent_call: bool = True) -> Table:
        for field_name in model.model_fields.keys():
            value = getattr(model, field_name)

            if isinstance(value, BaseModel):
                if not hasattr(value, 'id'):
                    setattr(table_entity, field_name, await self.create(value))
                    continue

                old_field_entity: Table | None = getattr(table_entity, field_name)
                if old_field_entity:
                    if old_field_entity.id == value.id:
                        await self.update(value, old_field_entity)
                        continue
                    else:
                        if self.config.delete_old_values:
                            await self.session.delete(old_field_entity)

                replaced_entity = await self.get(value._table_class, value.id)
                setattr(table_entity, field_name, await self.update(value, replaced_entity))

            elif isinstance(value, SUPPORTED_ITERABLES):
                value: Collection[BaseModel]
                old_field_entities: set[Table] = set(getattr(table_entity, field_name))
                mapped_orm_entities = await self.map_collection(value)
                entities_to_remove = old_field_entities - set(mapped_orm_entities)
                if self.config.delete_old_values:
                    for entity in entities_to_remove:
                        await self.session.delete(entity)
                setattr(table_entity, field_name, mapped_orm_entities)
            else:
                if not subsequent_call or self.config.allow_update:
                    setattr(table_entity, field_name, value)
        return table_entity

    async def get(self, table: type[Table], entity_id: int) -> Table:
        entity = await self.session.scalar(select(table).filter_by(id=entity_id))
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Entity {table} with id {entity_id} not found')
        return entity
