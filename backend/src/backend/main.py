import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.texts import router as texts_router
from backend.db.database import Base, engine
from backend.models.text import SelectedText
from backend.workers.retry_worker import retry_worker


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the retry worker when FastAPI starts
    worker_task = asyncio.create_task(retry_worker())

    yield

    # Stop the retry worker when FastAPI shuts down
    worker_task.cancel()

    try:
        await worker_task
    except asyncio.CancelledError:
        print("🛑 Retry worker stopped.")


app = FastAPI(
    title="Text Sync Backend",
    description="Backend for the Chrome Extension text sync system",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(texts_router)


@app.get("/")
def root():
    return {
        "success": True,
        "status": 200,
        "message": "Chrome Extension Backend is running!",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API Health is Awesome!",
    }