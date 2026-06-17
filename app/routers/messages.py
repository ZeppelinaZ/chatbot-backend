from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from database import DATABASE

router = APIRouter()

@router.get("/messages", response_model=list[ItemResponse])
async def list_items(skip: int = 0, limit: int = 100):
    """Получить список сообщений диалога"""
    items = DATABASE.query(Item).offset(skip).limit(limit).all()
    return items
