from logging.config import fileConfig

from sqlalchemy import create_engine, URL
from sqlalchemy import pool

from alembic import context

from bot_manager.tables import ManagerBase
from bot_manager.database import url_params


config = context.config

url_object = URL.create(
    'postgresql+psycopg2',
    **url_params
)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = ManagerBase.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=url_object,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(url_object, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
