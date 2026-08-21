from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.text import SelectedText


router = APIRouter(
    prefix = "/texts",
    tags = ["Texts"]
)


class TextCreate(BaseModel):
    content: str
    
    
@router.post("/")
def create_text(
    text: TextCreate,
    db: Session = Depends(get_db)
):
    new_text = SelectedText(
        content = text.content
    )
    
    
    db.add(new_text)
    db.commit()
    db.refresh(new_text)
    
    
    return {
        "message": "Text saved successfully",
        "data": {
            "id": new_text.id,
            "content": new_text.content,
            "status": new_text.status,
            "created_at": new_text.created_at
        }
    }