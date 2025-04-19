from datetime import datetime

class ai_assistant_upsert:
    def __init__(self, collection):
        self.collection = collection

    def obtener_o_crear_usuario_sin_mensaje(self,origen: str, identificador: str):
        actual_datetime = datetime.now().astimezone()

        # Buscar usuario existente por cualquier canal
        usuario_existente = self.collection.find_one({
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

            resultado = self.collection.insert_one(nuevo_usuario)
            print("Nuevo usuario creado sin mensaje.")
            return str(resultado.inserted_id),[]