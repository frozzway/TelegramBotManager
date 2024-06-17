from bot_manager import tables
from bot_manager.database import ManagerSession
from bot_manager.services.crud_service import CrudService


class BotService(CrudService):
    def __init__(self, session: ManagerSession):
        super().__init__(session, tables.Bot)
