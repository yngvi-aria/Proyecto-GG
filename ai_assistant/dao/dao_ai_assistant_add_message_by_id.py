from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId  # Para convertir el ID si viene como string


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