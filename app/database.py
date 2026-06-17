from sqlalchemy.orm import DeclarativeBase
import os

from app.providers import PostgresDBProvider

class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy моделей"""
    pass

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE = PostgresDBProvider(DATABASE_URL)
