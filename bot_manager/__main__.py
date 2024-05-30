import uvicorn

from bot_manager.settings import settings


uvicorn.run(
    'bot_manager:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
