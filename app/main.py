from fastapi import FastAPI
from app.api import chat, health, documents, dashboard
from app.core.database import engine, Base

# 自动创建数据库表（第一次运行会生成 app.db）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CX AI Knowledge Base")

app.include_router(chat.router)
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "AI Knowledge Base API is running"}