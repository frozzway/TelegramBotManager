FROM python:3.10-slim
WORKDIR /app

COPY requirements-linux.txt .

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements-linux.txt

COPY ./bot_manager bot_manager
COPY ./alembic_migrations alembic_migrations

CMD ["python", "-m", "bot_manager"]