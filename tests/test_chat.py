import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """测试健康检查接口"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_chat_api():
    """测试问答接口返回格式"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/chat/", json={"message": "你好"})
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert "sources" in data
        assert isinstance(data["reply"], str)

@pytest.mark.asyncio
async def test_dashboard_stats():
    """测试看板接口"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_chats" in data
        assert "hit_rate" in data