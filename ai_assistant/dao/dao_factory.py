from pymongo import MongoClient
from core.config import get_settings


class mongoCollection:    
    # === Configuración de conexión ===
    client = MongoClient(get_settings().MONGODB_URI)
    db = client[get_settings().DB_NAME]
    collection = db[get_settings().COLLECTION_NAME]

def get_connection():
    return mongoCollection.collection