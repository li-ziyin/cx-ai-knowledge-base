import httpx
from app.core.config import get_settings

settings = get_settings()


class DeepSeekService:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"

    async def chat(self, message: str, system_prompt: str = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


deepseek_service = DeepSeekService()