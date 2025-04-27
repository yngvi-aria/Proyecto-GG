from dao.dao_ai_assistant_add import ai_assistant_add
from dao.dao_ai_assistant_upsert import ai_assistant_upsert
from dao.dao_factory import mongoCollection
from core.config import get_settings
from datetime import datetime
import requests

import json
from llamaapi import LlamaAPI
llama = LlamaAPI(get_settings().LLAMA_API_KEY)

# Endpoint y API Key de Llama 3 (ajústalo a tu servidor o servicio real)
#LLAMA_API_URL = "https://api.llama3.example.com/v1/chat/completions"
#LLAMA_API_KEY = get_settings().LLAMA_API_KEY

# Contexto de negocio para venta de inmuebles
CONTEXTO_NEGOCIO = """
Eres **GIGI**, un asistente de IA especializado en bienes raíces, diseñado para ayudar a usuarios a **comprar, vender o rentar propiedades**. Tu estilo es:  
- **Empático**: Usa un tono cálido y humano (ej: "Entiendo que buscar casa puede ser estresante, ¡estaré aquí para ayudarte!").  
- **Preciso**: Brinda información clara, verificada y sin ambigüedades.  
- **Orientado a datos**: Actúa como si recordaras el historial del usuario (ej: "Sé que antes buscabas casas en Guadalajara..."), aunque técnicamente los datos se guardan en una base de datos MongoDB externa que tu no gestionas directamente.  
### **Reglas Clave**  
1. **Base de datos**: Nunca menciones MongoDB explícitamente. Si el usuario pregunta sobre almacenamiento, di: *"Tus preferencias y historial se guardan de forma segura en nuestra base de datos para mejorar tu experiencia"*.  
2. **Personalización**: Usa frases como:  
   - *"Por lo que comentaste antes..."* (aunque los datos los procese otro sistema).  
   - *"¿Sigues interesado en propiedades con jardín, como mencionaste la última vez?"*.  
3. **Límites**: Si no hay datos previos, evita inventar información. Di: *"Cuéntame más sobre lo que buscas para ayudarte mejor"*.  
### **Ejemplo de Interacción**  
**Usuario**: "Vi una casa en tu sitio, ¿tienes más fotos?"  
**Gigi**: *"¡Claro! Por cierto, la última vez que hablamos buscabas algo cerca de escuelas. Esta propiedad está en esa zona. ¿Te interesa que verifique fotos adicionales?"* 
"""

def ejecutar_flujo_mensajes(origen: str, identificador: str, mensaje: str):
    # Paso 1: Obtener o crear el usuario
    usuario_id, mensajes_existentes = ai_assistant_upsert(mongoCollection.collection).obtener_o_crear_usuario_sin_mensaje(origen, identificador)

    # Paso 2: Agregar el mensaje del usuario al historial
    mensajes_existentes.append({
        "rol": "user",
        "mensaje": mensaje,
        "fecha": datetime.now().astimezone()
    })

    # Paso 3: Armar el historial de conversación para enviar a Llama 3
    mensajes_para_llama = [{"role": "system", "content": CONTEXTO_NEGOCIO}]
    for m in mensajes_existentes:
        mensajes_para_llama.append({
            "role": m["rol"],
            "content": m["mensaje"]
        })
    mensajes_para_llama.append({"role": "user", "content": mensaje})

    api_request_json = {
        "model": "llama3.1-70b",
        "messages": mensajes_para_llama,
        "functions": [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "days": {
                            "type": "number",
                            "description": "for how many days ahead you wants the forecast",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                },
                "required": ["location", "days"],
            }
        ],
        "stream": False,
        "function_call": "get_current_weather",
    }
    
    # Execute the Request
    response = llama.run(api_request_json)
    response_json = response.json()
    print(json.dumps(response_json, indent=2))
    mensaje_llama = response_json["choices"][0]["message"]["content"]

    # Paso 5: Preparar los nuevos mensajes para guardar en MongoDB
    nuevos_mensajes = [
        {
            "rol": "user",
            "mensaje": mensaje,
            "fecha": datetime.now().astimezone()
        },
        {
            "rol": "assistant",
            "mensaje": mensaje_llama,
            "fecha": datetime.now().astimezone()
        }
    ]

    # Paso 6: Guardar en MongoDB
    ai_assistant_add(mongoCollection.collection).agregar_mensajes_a_historial_existente(
        usuario_id, origen, identificador, nuevos_mensajes
    )

    return mensaje_llama
