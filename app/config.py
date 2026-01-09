from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "AI DOMINATOR - Core Engine"
    VERSION: str = "v1.0.0-GEMINI"
    API_PREFIX: str = "/api/v1"
    
    # مفتاح جوجل (يتم قراءته من Render Environment)
    GOOGLE_API_KEY: str = "PLACEHOLDER_KEY" 

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
