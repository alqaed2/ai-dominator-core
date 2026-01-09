from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "AI DOMINATOR - Core Engine"
    VERSION: str = "v1.0.0-ALPHA"
    API_PREFIX: str = "/api/v1"
    
    # مفاتيح الأمان (يتم تعيينها لاحقاً في Render)
    # حالياً نضع قيماً افتراضية للتشغيل الأولي
    OPENAI_API_KEY: str = "PLACEHOLDER_KEY" 
    MASTER_SECRET_KEY: str = "change_this_to_something_secure"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()