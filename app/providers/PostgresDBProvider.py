

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

# импорты моделей
from app.models.dialogue import Dialogue
from app.models.message import Message

class PostgresDBProvider:
    """Провайдер для работы с PostgreSQL базой данных"""
    def __init__(self, DATABASE_URL: str):
        self.engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        """Создать таблицы, если их нет"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_or_create_dialogue(self, chat_id: str, user_id: int) -> Dialogue:
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
                    last_active=datetime.now(),
                    status="active"
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

    async def append_message(self, chat_id: str, user_id: int, message: Message):
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
