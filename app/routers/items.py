from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.get("/items", response_model=list[ItemResponse])
async def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех элементов"""
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    """Создать новый элемент"""
    db_item = Item(**item_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Получить элемент по ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Element not found")
    return item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    """Обновить элемент"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Element not found")

    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Удалить элемент"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Element not found")

    db.delete(item)
    db.commit()
