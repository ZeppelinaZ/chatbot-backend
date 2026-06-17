from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.schemas.messages import MessageSchema

class DialogueSchema(BaseModel):
    id: UUID
    user_id: UUID
    messages: list[MessageSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
