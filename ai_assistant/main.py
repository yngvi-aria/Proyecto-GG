from api import api_ai_assistant_real_estate
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

origen="whatsapp"
identificador="+5215551234567"
mensaje="Hola buenas tardes"

class MensajeEntrada(BaseModel):
    origen: str
    identificador: str
    mensaje: str

@app.post("/asistente/inmobiliario")
def asistente_inmobiliario(datos: MensajeEntrada):
    mensaje_chatGPT=api_ai_assistant_real_estate.ejecutar_flujo_mensajes (datos.origen, datos.identificador, datos.mensaje)
    return {"respuesta": mensaje_chatGPT}