from fastapi import FastAPI

from backend.db.database import Base, engine
from backend.models.text import SelectedText


Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Text Sync Backend",
    description = "Backend for the chrome extension text sync system",
    version = "1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "status": 200,
        "message": "Chrome Extension Backend is running!"
        }
    
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API Health is Awesome!"
    }