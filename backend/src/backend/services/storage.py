import os

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
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "fields": {
            "content": content,
            "status": status,
            "retry_count": retry_count,
            "created_at": created_at,
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            AIRTABLE_URL,
            headers=headers,
            json=data,
        )

    response.raise_for_status()

    return response.json()