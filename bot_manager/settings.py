from pathlib import Path
from zoneinfo import ZoneInfo

from alembic.config import Config

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug_mode: bool = False

    project_name: str = 'BotManager'

    server_host: str = '0.0.0.0'
    server_port: int = '8080'
    timezone: str = 'Asia/Yekaterinburg'

    db_username: str = 'postgres'
    db_password: str = '123'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_database: str = 'TelegramBotManager'
    db_migrations_path: str = str(Path.cwd() / 'alembic_migrations')

    api_url: str = 'https://api.armgs.team/bot/v1'

    jwt_expires_s: int = 60 * 30
    jwt_refresh_token_expires_s: int = 60 * 60 * 24 * 7
    jwt_cookie_name: str = 'BotManager'
    jwt_secret: str = 'a99ef8a3a0734e2d820dc323a29b787235ab7ec504a870ca0ff8c9df5f058042'
    jwt_algorithm: str = 'HS256'

    hostname: str = 'example.com'
    email_server: str = ''
    email_sender: str = ''
    email_account: str = ''
    email_password: str = 'JMBNsbvuhknasdf7124'
    email_test_recipient: str = '<EMAIL>'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)

autofill = {
    'email_server': f'mail.{settings.hostname}',
    'email_sender': f'no-reply@{settings.hostname}',
    'email_account': f'no-reply@{settings.hostname}'
}

for key, value in autofill.items():
    if not getattr(settings, key, None):
        setattr(settings, key, value)


alembic_config_path = Path(settings.db_migrations_path) / "alembic.ini"
alembic_scripts_path = Path(settings.db_migrations_path) / "script"

alembic_cfg = Config(alembic_config_path)
alembic_cfg.set_main_option("script_location", str(alembic_scripts_path))

timezone = ZoneInfo(settings.timezone)
