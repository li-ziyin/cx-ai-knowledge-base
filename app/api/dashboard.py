from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.database_models import ChatLog, DocumentLog
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """数据统计看板"""
    total_chats = db.query(func.count(ChatLog.id)).scalar() or 0
    total_docs = db.query(func.count(DocumentLog.id)).scalar() or 0
    total_chunks = len(rag_service.chunks)

    # 检索命中率（有参考来源的问答占比）
    hit_chats = db.query(func.count(ChatLog.id)).filter(ChatLog.sources_count > 0).scalar() or 0
    hit_rate = round(hit_chats / total_chats * 100, 2) if total_chats > 0 else 0

    return {
        "total_chats": total_chats,
        "total_documents": total_docs,
        "total_chunks": total_chunks,
        "hit_rate": f"{hit_rate}%"
    }


@router.get("/recent-chats")
async def get_recent_chats(limit: int = 10, db: Session = Depends(get_db)):
    """最近问答记录"""
    logs = db.query(ChatLog).order_by(ChatLog.created_at.desc()).limit(limit).all()
    return [
        {
            "question": log.question,
            "answer": log.answer[:100] + "..." if len(log.answer) > 100 else log.answer,
            "sources_count": log.sources_count,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None
        }
        for log in logs
    ]