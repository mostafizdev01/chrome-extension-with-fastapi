from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.text import SelectedText
from backend.services.storage import save_to_airtable


router = APIRouter(
    prefix="/texts",
    tags=["Texts"],
)


class TextCreate(BaseModel):
    content: str


@router.post("/")
async def create_text(
    text: TextCreate,
    db: Session = Depends(get_db),
):
    new_text = SelectedText(
        content=text.content,
        status="pending",
    )

    # Step 1: Save text to local SQLite first
    db.add(new_text)
    db.commit()
    db.refresh(new_text)

    # Step 2: Try to save the text to Airtable
    try:
        await save_to_airtable(
            content=new_text.content,
            status="synced",
            retry_count=new_text.retry_count,
            created_at=new_text.created_at.isoformat(),
        )

        # Step 3: Airtable success
        new_text.status = "synced"
        new_text.last_error = None

        db.commit()
        db.refresh(new_text)

        return {
            "message": "Text saved and synced successfully",
            "data": {
                "id": new_text.id,
                "content": new_text.content,
                "status": new_text.status,
                "retry_count": new_text.retry_count,
                "created_at": new_text.created_at,
            },
        }

    except Exception as error:
        # Step 4: Airtable failed
        new_text.status = "pending"
        new_text.retry_count += 1
        new_text.last_error = str(error)

        db.commit()
        db.refresh(new_text)

        return {
            "message": "Text saved locally. Airtable sync failed and will be retried.",
            "data": {
                "id": new_text.id,
                "content": new_text.content,
                "status": new_text.status,
                "retry_count": new_text.retry_count,
                "last_error": new_text.last_error,
                "created_at": new_text.created_at,
            },
        }


@router.get("/")
def get_texts(
    db: Session = Depends(get_db),
):
    texts = db.query(SelectedText).all()

    return {
        "message": "Texts retrieved successfully",
        "data": texts,
    }