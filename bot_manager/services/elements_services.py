from bot_manager.services.crud_service import CrudService
from bot_manager.services.db_dependency import BotSession
from bot_manager import tables


class LinkButtonService(CrudService):
    def __init__(self, session: BotSession):
        super().__init__(session, tables.LinkButton)


class CategoryService(CrudService):
    def __init__(self, session: BotSession):
        super().__init__(session, tables.Category)


class ScenarioService(CrudService):
    def __init__(self, session: BotSession):
        super().__init__(session, tables.ScenarioButton)
