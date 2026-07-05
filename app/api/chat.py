from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.deepseek_service import deepseek_service
from app.services.rag_service import rag_service
from app.models.database_models import ChatLog

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = None


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. 检索
    contexts = rag_service.search(request.message, top_k=3)

    # 2. 构建 Prompt
    # 2. 构建 Prompt
    if contexts:
        context_text = "\n\n".join([f"参考资料{i + 1}:\n{c}" for i, c in enumerate(contexts)])
        prompt = f"""请基于以下参考资料回答用户问题。

    参考资料：
    {context_text}

    用户问题：{request.message}

    请直接根据以上资料回答，不要添加资料外的信息。如果资料中有相关信息，请务必基于资料回答。

    回答："""
    else:
        prompt = request.message
        contexts = []

    # 3. 调用 DeepSeek
    system = request.system_prompt or "你是企业知识库助手，基于资料回答问题。"
    reply = await deepseek_service.chat(message=prompt, system_prompt=system)

    # 4. 记录日志到数据库
    log = ChatLog(
        question=request.message,
        answer=reply,
        sources_count=len(contexts)
    )
    db.add(log)
    db.commit()

    return ChatResponse(reply=reply, sources=contexts)