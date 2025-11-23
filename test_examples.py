"""
Ejemplos adicionales de uso de WhatsApp Business API
"""

from whatsapp_sender import WhatsAppSender
import os
from dotenv import load_dotenv

load_dotenv()


def ejemplo_mensaje_utilidad():
    """Ejemplo de mensaje de utilidad usando template"""
    sender = WhatsAppSender()
    phone = os.getenv('YOUR_PHONE_NUMBER')
    
    # Ejemplo: Enviar template de utilidad usando hello_world (template por defecto de Meta)
    try:
        result = sender.send_utility_message(
            to=phone,
            template_name="hello_world",  # Template por defecto de Meta
            parameters=None,  # hello_world no requiere parámetros
            language_code="es"
        )
        print("✅ Mensaje de utilidad (template) enviado")
        print(f"ID: {result.get('messages', [{}])[0].get('id')}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_mensaje_servicio():
    """Ejemplo de mensaje de servicio"""
    sender = WhatsAppSender()
    phone = os.getenv('YOUR_PHONE_NUMBER')
    
    mensaje = """
🛎️ Mensaje de Servicio

Hola! Gracias por contactarnos.

Nuestro equipo de soporte está disponible para ayudarte.
Horario: Lunes a Viernes, 9:00 - 18:00

¿En qué podemos asistirte?
"""
    
    try:
        result = sender.send_service_message(phone, mensaje.strip())
        print("✅ Mensaje de servicio enviado")
        print(f"ID: {result.get('messages', [{}])[0].get('id')}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_mensaje_personalizado():
    """Ejemplo de mensaje personalizado con tipo específico"""
    sender = WhatsAppSender()
    phone = os.getenv('YOUR_PHONE_NUMBER')
    
    # Puedes especificar el tipo directamente
    mensaje = "Este es un mensaje personalizado de tipo utility"
    
    try:
        result = sender.send_text_message(phone, mensaje, message_type="utility")
        print("✅ Mensaje personalizado enviado")
        print(f"ID: {result.get('messages', [{}])[0].get('id')}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🧪 Ejemplos de uso de WhatsApp Business API\n")
    
    print("\n1️⃣ Ejemplo: Mensaje de Utilidad")
    ejemplo_mensaje_utilidad()
    
    print("\n2️⃣ Ejemplo: Mensaje de Servicio")
    ejemplo_mensaje_servicio()
    
    print("\n3️⃣ Ejemplo: Mensaje Personalizado")
    ejemplo_mensaje_personalizado()
    
    print("\n✨ Ejemplos completados!")

