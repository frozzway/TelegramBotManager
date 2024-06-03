from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = '8080'
    timezone: str = 'Asia/Yekaterinburg'

    db_username: str = 'postgres'
    db_password: str = '123'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_database: str = 'TelegramBotManager'

    api_url: str = 'https://api.armgs.team/bot/v1'

    jwt_expires_s: int = 60 * 30
    jwt_refresh_token_expires_s: int = 60 * 60 * 24 * 7
    jwt_cookie_name: str = 'BotController'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
