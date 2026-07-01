from fastapi import APIRouter
from pydantic import BaseModel
from app.services.deepseek_service import deepseek_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    system_prompt: str = None


class ChatResponse(BaseModel):
    reply: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await deepseek_service.chat(
        message=request.message,
        system_prompt=request.system_prompt
    )
    return ChatResponse(reply=reply)
