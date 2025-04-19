from pymongo import MongoClient
from ai_assistant.core.config import get_settings

settings = get_settings()

# === Configuración de conexión ===
client = MongoClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

def get_connection():
    return collection