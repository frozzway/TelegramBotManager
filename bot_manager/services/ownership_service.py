from fastapi import HTTPException, status
from sqlalchemy import select

from bot_manager.models import Ownership
from bot_manager.services.db_dependency import BotSession
from bot_manager import tables


class OwnershipService:
    def __init__(self, session: BotSession):
        self.session = session

    async def set_ownership(self, owner_id: int, data: list[list[Ownership]]) -> None:
        """Установить принадлежность элементов категории с учетом позиции"""
        await self._remove_ownerships(owner_id)
        available_categories = await self.get_available_categories(owner_id)
        available_categories_ids = {c.id for c in available_categories}
        for position_y, elements_row in enumerate(data):
            for position_x, element in enumerate(elements_row):
                if element.element_type == 'Category':
                    if element.element_id not in available_categories_ids:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category is not available')
                    ownership = tables.Ownership(category_id=element.element_id)
                else:
                    ownership = tables.Ownership(button_id=element.element_id)
                ownership.owner_category_id = owner_id
                ownership.position_y = position_y + 1
                if len(elements_row) > 1:
                    ownership.position_x = position_x + 1
                self.session.add(ownership)
        await self.session.commit()

    async def _remove_ownerships(self, owner_id: int) -> None:
        ownerships = await self.session.scalars(
            select(tables.Ownership)
            .where(tables.Ownership.owner_category_id == owner_id)
        )
        for ownership in ownerships:
            await self.session.delete(ownership)

    async def get_available_categories(self, owner_id: int) -> list[tables.Category]:
        """Получить категории, которые можно отнести к категории с идентификатором ``owner_id``."""
        categories = await self.session.scalars(select(tables.Category))

        s = (
            select(tables.Ownership.owner_category_id)
            .where(tables.Ownership.category_id == owner_id)
        ).cte(recursive=True)

        s2 = s.union(
            select(tables.Ownership.owner_category_id)
            .join(s, tables.Ownership.category_id == s.c.owner_category_id)
        )

        stmt = select(s2.c.owner_category_id)
        top_categories = set(await self.session.scalars(stmt))
        available_categories = [c for c in categories if c.id not in top_categories and c.id != owner_id]

        return available_categories

