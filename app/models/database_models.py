from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base
from datetime import datetime

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500))
    answer = Column(Text)
    sources_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

class DocumentLog(Base):
    __tablename__ = "document_logs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    chunks_added = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)