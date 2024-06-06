from pathlib import Path

from alembic.config import Config

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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
    jwt_cookie_name: str = 'BotController'
    jwt_secret: str = 'a99ef8a3a0734e2d820dc323a29b787235ab7ec504a870ca0ff8c9df5f058042'
    jwt_algorithm: str = 'HS256'

    hostname: str = 'example.com'
    email_server: str = f'mail.{hostname}'
    email_sender: str = f'no-reply@{hostname}'
    email_account: str = f'no-reply@{hostname}'
    email_password: str = 'JMBNsbvuhknasdf7124'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)

alembic_config_path = Path(settings.db_migrations_path) / "alembic.ini"
alembic_scripts_path = Path(settings.db_migrations_path) / "script"

alembic_cfg = Config(alembic_config_path)
alembic_cfg.set_main_option("script_location", str(alembic_scripts_path))
