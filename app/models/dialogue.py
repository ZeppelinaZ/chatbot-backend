from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Dialogue(Base):
    __tablename__ = "dialogues"

    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    messages = Column(JSON, default=list)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
