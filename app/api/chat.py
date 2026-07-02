from fastapi import APIRouter
from pydantic import BaseModel
from app.services.deepseek_service import deepseek_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = None


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. 检索相关文档
    contexts = rag_service.search(request.message, top_k=3)

    # 2. 构建 RAG Prompt
    if contexts:
        context_text = "\n\n".join([f"参考资料{i + 1}:\n{c}" for i, c in enumerate(contexts)])
        prompt = f"""基于以下参考资料回答问题。如果资料中没有相关信息，请说"根据现有资料无法回答"。

{context_text}

用户问题: {request.message}

请回答:"""
    else:
        prompt = request.message
        contexts = []

    # 3. 调用 DeepSeek
    system = request.system_prompt or "你是企业知识库助手，基于资料回答问题。"
    reply = await deepseek_service.chat(message=prompt, system_prompt=system)

    return ChatResponse(reply=reply, sources=contexts)