from fastapi import APIRouter, Depends, HTTPException
import uuid

from app.schemas.dialogue import DialogueSchema
from app.db.database import DATABASE

router = APIRouter()

@router.get("/dialogue", response_model=list[DialogueSchema])
async def list_dialogues(user_id: str):
    """Получить список диалогов"""
    dialogues = await DATABASE.get_dialogues_by_user_id(user_id)
    return dialogues

@router.post("/dialogue", response_model=DialogueSchema)
async def create_dialogue(user_id):
    """Создать новый элемент"""
    chat_id = str(uuid.uuid4())
    newDialogue = await DATABASE.get_or_create_dialogue(chat_id, user_id)
    return newDialogue


# @router.get("/items/{item_id}", response_model=ItemResponse)
# async def get_item(item_id: int, db: Session = Depends(get_db)):
#     """Получить элемент по ID"""
#     item = db.query(Item).filter(Item.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Element not found")
#     return item


# @router.put("/items/{item_id}", response_model=ItemResponse)
# async def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
#     """Обновить элемент"""
#     item = db.query(Item).filter(Item.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Element not found")

#     for field, value in item_data.model_dump(exclude_unset=True).items():
#         setattr(item, field, value)

#     db.commit()
#     db.refresh(item)
#     return item


# @router.delete("/items/{item_id}", status_code=204)
# async def delete_item(item_id: int, db: Session = Depends(get_db)):
#     """Удалить элемент"""
#     item = db.query(Item).filter(Item.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Element not found")

#     db.delete(item)
#     db.commit()
