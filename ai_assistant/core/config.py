from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str
    mongodb_uri: str

    class Config:
        env_file = ".env"  # Indica que las variables están en un archivo .env

@lru_cache()
def get_settings():
    return Settings()