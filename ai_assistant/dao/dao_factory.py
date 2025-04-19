from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId  # Para convertir el ID si viene como string

# === Configuración de conexión ===
MONGO_URI = "mongodb+srv://ai_assistan_user_phyton:111Nfdgalye@cluster0.gfi5cti.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "gigi_real_estate"
COLLECTION_NAME = "ai_assistant"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_connection():
    return collection