from fastapi import FastAPI
from pony.orm import db_session, Database

from .models import db


def register_pony_orm(app: FastAPI, config: dict, generate_schemas: bool = False) -> None:
    # Инициализация соединения с базой данных
    db.bind(**config['connections']['default'])
    if generate_schemas:
        db.generate_mapping(create_tables=True)  # Вызывается после db.bind()

    @app.on_event("startup")
    async def init_orm():
        # Открытие сессии при старте приложения
        db_session.__enter__()

    @app.on_event("shutdown")
    async def close_orm():
        # Закрытие сессии при остановке приложения
        db_session.__exit__(None, None, None)
