from api import api_ai_deepseek
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

@app.post("/assistent/deepseek")
def asistente_deepseek(datos: MensajeEntrada):
    mensaje_chatGPT=api_ai_deepseek.ejecutar_flujo_mensajes (datos.origen, datos.identificador, datos.mensaje)
    return {"respuesta": mensaje_chatGPT}