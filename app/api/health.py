from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("/")
async def health_check():
    return {"status": "ok", "service": "cx-ai-knowledge-base"}