from bot_manager.services.crud_service import CrudService
from bot_manager.services.db_dep import BotSession
from bot_manager import tables


class CategoryService(CrudService):
    def __init__(self, session: BotSession):
        super().__init__(session, tables.Category)

