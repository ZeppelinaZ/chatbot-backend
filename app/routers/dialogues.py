from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID, uuid4

from app.dialogue import DialogueSchema, DialoguesSchema
from app.database import DATABASE

router = APIRouter()

@router.get("/dialogues", response_model=DialoguesSchema)
async def list_dialogues(user_id: UUID):
    """Получить список диалогов для user_id"""
    dialogues = await DATABASE.get_dialogues(user_id)
    return dialogues


@router.post("/dialogue", response_model=DialogueSchema)
async def create_dialogue(user_id: UUID):
    """Создать новый диалог для user_id"""
    chat_id = str(uuid4())
    new_dialogue = await DATABASE.create_dialogue(chat_id, user_id)
    return new_dialogue


@router.delete("/dialogue", response_model=UUID)
async def delete_dialogue(chat_id: UUID):
    """Удалить диалог по chat_id"""


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
