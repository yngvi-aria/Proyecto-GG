from api import api_ai_deepseek
from api import api_ai_openAI
from api import api_ai_llama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MensajeEntrada(BaseModel):
    origen: str
    identificador: str
    mensaje: str

@app.post("/assistent/deepseek")
def asistente_deepseek(datos: MensajeEntrada):
    mensaje_deepseek=api_ai_deepseek.ejecutar_flujo_mensajes (datos.origen, datos.identificador, datos.mensaje)
    return {"respuesta": mensaje_deepseek}

@app.post("/assistent/chatgpt")
def asistente_chatgpt(datos: MensajeEntrada):
    mensaje_chatGPT=api_ai_openAI.ejecutar_flujo_mensajes (datos.origen, datos.identificador, datos.mensaje)
    return {"respuesta": mensaje_chatGPT}

@app.post("/assistent/llama3")
def asistente_chatgpt(datos: MensajeEntrada):
    mensaje_llama=api_ai_llama.ejecutar_flujo_mensajes (datos.origen, datos.identificador, datos.mensaje)
    return {"respuesta": mensaje_llama}
