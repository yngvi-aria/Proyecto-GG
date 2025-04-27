from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MONGODB_URI: str
    DB_NAME: str
    COLLECTION_NAME: str
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_URL: str
    LLAMA_API_KEY: str

    class Config:
        env_file = ".env"  # Indica que las variables están en un archivo .env
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()