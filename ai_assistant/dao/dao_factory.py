from datetime import datetime
from pymongo import MongoClient
from core.config import get_settings
from bson import ObjectId  # Para convertir el ID si viene como string

settings = get_settings()

# === Configuración de conexión ===
MONGO_URI = settings.mongodb_uri
DB_NAME = "gigi_real_estate"
COLLECTION_NAME = "ai_assistant"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_connection():
    return collection