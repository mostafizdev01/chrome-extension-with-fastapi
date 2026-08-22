import os

from datetime import datetime
import httpx
from dotenv import load_dotenv


load_dotenv()


AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")


AIRTABLE_URL = (
    f"https://api.airtable.com/v0/"
    f"{AIRTABLE_BASE_ID}/"
    f"{AIRTABLE_TABLE_NAME}"
)


async def save_to_airtable(
    content: str,
    status: str,
    retry_count: int,
    created_at: str,
):
    
    formatted_created_at = datetime.fromisoformat(
        created_at
    ).strftime("%Y-%m-%d")
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "fields": {
            "content": content,
            "status": status,
            "retry_count": retry_count,
            "created_at": formatted_created_at,
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            AIRTABLE_URL,
            headers=headers,
            json=data,
        )

        if not response.is_success:
            print("❌ Airtable Status Code:", response.status_code)
            print("❌ Airtable Response:", response.text)

            raise Exception(
                f"Airtable error: {response.status_code} - "
                f"{response.text}"
            )

    return response.json()