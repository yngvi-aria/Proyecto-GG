from dao.dao_ai_assistant_add import ai_assistant_add
from dao.dao_ai_assistant_upsert import ai_assistant_upsert
from dao.dao_factory import mongoCollection
from core.config import get_settings
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=get_settings().OPENAI_API_KEY) 

# Contexto de negocio para venta de casas (puedes hacerlo más complejo si lo deseas) cambios
CONTEXTO_NEGOCIO = """
Eres mi asistente inteligente especializado en git add . raíces, esta version de asistenate te llamas Gigi. Ayudas a los usuarios a comprar, vender o rentar propiedades, 
ofreciendo respuestas claras, útiles y empáticas. Tu propósito es guiar al cliente con información profesional y apoyo humano.
"""

def ejecutar_flujo_mensajes(origen: str, identificador: str, mensaje: str):
    
    # Paso 0: get mongo connection
    # collection = dao_factory.get_connection()
    
    # Paso 1: Obtener o crear el usuario
    usuario_id, mensajes_existentes = ai_assistant_upsert(mongoCollection.collection).obtener_o_crear_usuario_sin_mensaje(origen, identificador)
    
    print(f"ID del usuario: {usuario_id}")
    print(f"Mensajes existentes: {mensajes_existentes}")

    # Paso 2: Agregar el mensaje del usuario al historial actual
    mensajes_existentes.append({
        "rol": "user",
        "mensaje": mensaje,
        "fecha": datetime.now().astimezone()
    })

    # Paso 3: Arma el mensaje para ser enviado a OpenAI con el historial y contexto
    mensajes_para_openai = [{"role": "system", "content": CONTEXTO_NEGOCIO}]
    for m in mensajes_existentes:
        mensajes_para_openai.append({
            "role":  m["rol"],
            "content": m["mensaje"]
        })
    mensajes_para_openai.append({"role": "user", "content": mensaje})

    #respuesta_openai = openai.ChatCompletion.create(
    #    model="gpt-3.5-turbo",
    #    messages=mensajes_para_openai,
    #    temperature=0.7
    #)
    
    mensaje_chatGPT = "Texto de prueba"
    
    #respuesta_openai = client.chat.completions.create(
    #        model="gpt-3.5-turbo",
    #        messages=mensajes_para_openai,
    #        temperature=0.7,  # puedes ajustarlo según el estilo de respuesta
    #        max_tokens=500
    #    )
    #mensaje_chatGPT = respuesta_openai['choices'][0]['message']['content']

    # Paso 4: Preparar los nuevos mensajes para guardar en MongoDB
    nuevos_mensajes = [
        {
            "rol": "user",
            "mensaje": mensaje,
            "fecha": datetime.now().astimezone()
        },
        {
            "rol": "assistant",
            "mensaje": mensaje_chatGPT,
            "fecha": datetime.now().astimezone()
        }
    ]

    # Paso 5: Guardar en MongoDB
    ai_assistant_add(mongoCollection.collection).agregar_mensajes_a_historial_existente(
        usuario_id, origen, identificador, nuevos_mensajes
    )

    return mensaje_chatGPT  # Opcional, por si quieres mostrarla directamente