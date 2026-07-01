from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "CX AI Knowledge Base"
    debug: bool = True
    deepseek_api_key: str = ""
    database_url: str = "sqlite:///./data/app.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()