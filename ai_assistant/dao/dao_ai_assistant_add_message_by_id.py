from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId  # Para convertir el ID si viene como string

# === Configuración de conexión ===
#MONGO_URI = "mongodb+srv://ai_assistan_user_phyton:111Nfdgalye@cluster0.gfi5cti.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#DB_NAME = "gigi_real_estate"
#COLLECTION_NAME = "ai_assistant"

#client = MongoClient(MONGO_URI)
#db = client[DB_NAME]
#collection = db[COLLECTION_NAME]

def agregar_mensajes_a_historial_existente(collection,usuario_id, origen: str, identificador: str, mensajes: list):

    actual_datetime = datetime.now().astimezone()
    
    # Convertimos el ID a ObjectId si viene como string
    if isinstance(usuario_id, str):
        usuario_id = ObjectId(usuario_id)

    resultado = collection.update_one(
        {
            "_id": usuario_id,
            "historiales.origen": origen,
            "historiales.identificador": identificador
        },
        {
            "$push": {"historiales.$.mensajes": {"$each": mensajes}},
            "$set": {"ultima_interaccion": actual_datetime}
        }
    )

    if resultado.modified_count > 0:
        print(f"Se agregaron {len(mensajes)} mensaje(s) al historial del usuario.")
    else:
        print("No se pudo agregar el mensaje. Verifica que el historial exista.")