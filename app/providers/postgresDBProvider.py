

from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# импорты моделей
from app.models.dialogue import Dialogue

class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy моделей"""
    pass

class PostgresDBProvider:
    """Провайдер для работы с базой данных PostgreSQL"""
    def __init__(self, DATABASE_URL: str):
        # что такое __init__
        self.engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        print("INIT DB CALLED")
        """Создать таблицы, если их нет"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_or_create_dialogue(self, chat_id: str, user_id: int) -> Dialogue:
        """Создать или получить диалог по chat_id"""
        async with self.SessionLocal() as session:
            dialogue = await session.execute(
                Dialogue.__table__.select().where(Dialogue.chat_id == chat_id)
            )
            dialogue = dialogue.first()  # None если нет
            if not dialogue:
                dialogue = Dialogue(
                    chat_id=chat_id,
                    user_id=user_id,
                    messages=[],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                session.add(dialogue)
                await session.commit()
                await session.refresh(dialogue)
            return dialogue.messages

    async def get_dialogues_by_user_id(self, user_id: int) -> list[Dialogue]:
        """Получение всего списка диалогов"""
        async with self.SessionLocal() as session:
            dialogues = await session.execute(
                Dialogue.__table__.select().where(Dialogue.user_id == user_id)
            )
            return dialogues
        
    async def delete_dialogue(self, chat_id: str):
        """Удалить диалог по chat_id"""
        async with self.SessionLocal() as session:
            dialogue = await session.execute(
                Dialogue.__table__.select().where(Dialogue.chat_id == chat_id)
            )
            row = dialogue.first()
            if row:
                await session.execute(
                    Dialogue.__table__.delete().where(Dialogue.chat_id == chat_id)
                )
                await session.commit()

    async def append_message(self, chat_id: str, user_id: int, message: JSON):
        now = datetime.now()
        async with self.SessionLocal() as session:
            dialogue = await session.execute(
                Dialogue.__table__.select().where(Dialogue.chat_id == chat_id)
            )
            row = dialogue.first()

            if row:
                dialogue_obj = Dialogue(**row._mapping)
                messages = dialogue_obj.messages or []
                messages.append({
                    "content": message.content,
                    "timestamp": now.isoformat(),
                    "role": message.role,
                    "visible_for_bot": message.visible_for_bot,
                    "visible_for_user": message.visible_for_user
                })

                await session.execute(
                    Dialogue.__table__.update()
                    .where(Dialogue.chat_id == chat_id)
                    .values(messages=messages, last_active=now)
                )
                await session.commit()
            else:
                new_dialogue = Dialogue(
                    chat_id=chat_id,
                    user_id=user_id,
                    messages=[{
                        "content": message.content,
                        "timestamp": now.isoformat(),
                        "role": message.role,
                        "visible_for_bot": message.visible_for_bot,
                        "visible_for_user": message.visible_for_user
                    }],
                    last_active=now,
                    status="active"
                )
                session.add(new_dialogue)
                await session.commit()
