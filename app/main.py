from fastapi import FastAPI
from app.api import chat, health, documents

app = FastAPI(title="CX AI Knowledge Base")

app.include_router(chat.router)
app.include_router(health.router)
app.include_router(documents.router)

@app.get("/")
async def root():
    return {"message": "AI Knowledge Base API is running"}