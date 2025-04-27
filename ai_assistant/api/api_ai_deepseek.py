from dao.dao_ai_assistant_add import ai_assistant_add
from dao.dao_ai_assistant_upsert import ai_assistant_upsert
from dao.dao_factory import mongoCollection
from core.config import get_settings
from datetime import datetime
import requests  # Para llamadas HTTP a la API de DeepSeek

# Configuración (ajusta según la API de DeepSeek)
# DEEPSEEK_API_KEY = get_settings().DEEPSEEK_API_KEY  # Si existe
# DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Ejemplo hipotético

# Contexto de negocio (sin cambios)
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
    # Paso 1: Obtener o crear el usuario (sin cambios)
    print ("##### Nuevo mensaje recibiro por API Deepseek:" + mensaje)
    
    usuario_id, mensajes_existentes = ai_assistant_upsert(mongoCollection.collection).obtener_o_crear_usuario_sin_mensaje(origen, identificador)
    
    # Paso 2: Agregar mensaje del usuario al historial (sin cambios)
    mensajes_existentes.append({
        "rol": "user",
        "mensaje": mensaje,
        "fecha": datetime.now().astimezone()
    })

    # Paso 3: Preparar mensajes para DeepSeek (similar a OpenAI)
    mensajes_para_deepseek = [{"role": "system", "content": CONTEXTO_NEGOCIO}]
    for m in mensajes_existentes:
        mensajes_para_deepseek.append({
            "role": m["rol"],
            "content": m["mensaje"]
        })
    
    # --- Opción 1: Usando API oficial de DeepSeek (si estuviera disponible) ---
    headers = {
        "Authorization": f"Bearer {get_settings().DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # Ajusta según el modelo
        "messages": mensajes_para_deepseek,
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(get_settings().DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        mensaje_deepseek = response.json()["choices"][0]["message"]["content"]
        #mensaje_deepseek = "respuesta de prueba"
    except Exception as e:
        error_msg = f"Error de conexión con DeepSeek API: {str(e)}"
        print(error_msg)
        mensaje_deepseek = error_msg
    
    # --- Opción 2: Si no hay API oficial (usar WebSocket o alternativa) ---
    # Puedes implementar una solución con selenium/puppeteer para interactuar con la web de DeepSeek.
    # Ejemplo simplificado:
    # mensaje_deepseek = simulate_deepseek_web_interaction(mensajes_para_deepseek)

    # Paso 4 y 5: Guardar en MongoDB (sin cambios, pero con mensaje_deepseek)
    nuevos_mensajes = [
        {
            "rol": "user",
            "mensaje": mensaje,
            "fecha": datetime.now().astimezone()
        },
        {
            "rol": "assistant",
            "mensaje": mensaje_deepseek,
            "fecha": datetime.now().astimezone()
        }
    ]
    
    ai_assistant_add(mongoCollection.collection).agregar_mensajes_a_historial_existente(
        usuario_id, origen, identificador, nuevos_mensajes
    )

    return mensaje_deepseek