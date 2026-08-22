import asyncio

from backend.db.database import SessionLocal
from backend.services.retry import retry_pending_texts


RETRY_INTERVAL = 30


async def retry_worker():
    print("🔄 Retry worker started.")

    while True:
        db = SessionLocal()

        try:
            result = await retry_pending_texts(db)

            print(
                "🔄 Retry result:",
                result,
            )

        except Exception as error:
            print(
                "❌ Retry worker error:",
                error,
            )

        finally:
            db.close()

        await asyncio.sleep(RETRY_INTERVAL)