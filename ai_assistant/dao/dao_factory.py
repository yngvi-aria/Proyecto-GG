from datetime import datetime
from pymongo import MongoClient
from ai_assistant.core.config import get_settings

settings = get_settings()

# === Configuración de conexión ===
MONGO_URI = settings.MONGODB_URI
DB_NAME = "gigi_real_estate"
COLLECTION_NAME = "ai_assistant"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_connection():
    return collection