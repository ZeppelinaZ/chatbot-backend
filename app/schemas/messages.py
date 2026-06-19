from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class MessageSchema(BaseModel):
    message_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    role: str

    class Config:
        from_attributes = True
