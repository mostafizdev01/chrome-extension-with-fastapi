from sqlalchemy.orm import Session

from backend.models.text import SelectedText
from backend.services.storage import save_to_airtable


async def retry_pending_texts(db: Session):
    pending_texts = (
        db.query(SelectedText)
        .filter(SelectedText.status == "pending")
        .all()
    )

    if not pending_texts:
        return {
            "message": "No pending texts found.",
            "retried": 0,
        }

    retried_count = 0
    synced_count = 0
    failed_count = 0

    for text in pending_texts:
        retried_count += 1

        try:
            await save_to_airtable(
                content=text.content,
                status="synced",
                retry_count=text.retry_count,
                created_at=text.created_at.isoformat(),
            )

            # Retry successful
            text.status = "synced"
            text.last_error = None

            db.commit()
            db.refresh(text)

            synced_count += 1

        except Exception as error:
            # Retry failed again
            text.retry_count += 1
            text.last_error = str(error)

            db.commit()
            db.refresh(text)

            failed_count += 1

    return {
        "message": "Retry process completed.",
        "retried": retried_count,
        "synced": synced_count,
        "failed": failed_count,
    }