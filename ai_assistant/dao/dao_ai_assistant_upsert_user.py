from pymongo import MongoClient
from datetime import datetime

# === Configuración de conexión ===
#MONGO_URI = "mongodb+srv://ai_assistan_user_phyton:111Nfdgalye@cluster0.gfi5cti.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#DB_NAME = "gigi_real_estate"
#COLLECTION_NAME = "ai_assistant"

#client = MongoClient(MONGO_URI)
#db = client[DB_NAME]
#collection = db[COLLECTION_NAME]

def obtener_o_crear_usuario_sin_mensaje(collection,origen: str, identificador: str):
    actual_datetime = datetime.now().astimezone()

    # Buscar usuario existente por cualquier canal
    usuario_existente = collection.find_one({
        "$or": [
            {"numeros_whatsapp": {"$in": [identificador]}},
            {"cuentas_instagram": {"$in": [identificador]}},
            {"cuentas_facebook": {"$in": [identificador]}}
        ]
    })

    if usuario_existente:
        historiales = usuario_existente.get("historiales", [])
        historial_existente = next((h for h in historiales if h["origen"] == origen and h["identificador"] == identificador), None)

        mensajes = historial_existente["mensajes"] if historial_existente else []
        return str(usuario_existente["_id"]), mensajes

    else:
        # Crear nuevo usuario sin mensajes
        nuevo_usuario = {
            "nombre": "Juan Pérez",
            "numeros_whatsapp": [identificador] if origen == "whatsapp" else [],
            "cuentas_instagram": [identificador] if origen == "instagram" else [],
            "cuentas_facebook": [identificador] if origen == "facebook" else [],
            "fecha_creacion": actual_datetime,
            "ultima_interaccion": actual_datetime,
            "historiales": [
                {
                    "origen": origen,
                    "identificador": identificador,
                    "mensajes": []
                }
            ],
            "etiquetas": ["cliente nuevo", "lead"]
        }

        resultado = collection.insert_one(nuevo_usuario)
        print("Nuevo usuario creado sin mensaje.")
        return str(resultado.inserted_id),[]