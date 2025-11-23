"""
Script para enviar mensajes de WhatsApp desde la terminal
Uso: python mandar_msg.py [free|template]
"""

import sys
import os
from whatsapp_sender import WhatsAppSender
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()


def send_free_message():
    """Envía un mensaje de texto libre (free)"""
    try:
        sender = WhatsAppSender()
        
        # Obtener número de teléfono
        phone = os.getenv('YOUR_PHONE_NUMBER')
        if not phone:
            phone = input("Ingresa el número de teléfono (código_país + número): ")
        
        # Obtener mensaje
        print("\n📝 Ingresa el mensaje a enviar (presiona Enter dos veces para finalizar):")
        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            if line:
                lines.append(line)
        
        message = "\n".join(lines)
        
        if not message.strip():
            print("❌ El mensaje no puede estar vacío")
            return
        
        print("\n📤 Enviando mensaje libre...")
        result = sender.send_text_message(phone, message)
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")


def send_template_message():
    """Envía un mensaje usando una plantilla (template)"""
    try:
        sender = WhatsAppSender()
        
        # Obtener número de teléfono
        phone = os.getenv('YOUR_PHONE_NUMBER')
        if not phone:
            phone = input("Ingresa el número de teléfono (código_país + número): ")
        
        # Obtener nombre de la plantilla
        template_name = input("\n📋 Ingresa el nombre de la plantilla: ").strip()
        if not template_name:
            print("❌ El nombre de la plantilla no puede estar vacío")
            return
        
        # Obtener código de idioma (opcional)
        language_code = input("🌐 Ingresa el código de idioma (presiona Enter para 'es'): ").strip()
        if not language_code:
            language_code = "es"
        
        # Preguntar si tiene componentes/parámetros
        has_components = input("\n¿La plantilla tiene parámetros? (s/n): ").strip().lower()
        components = None
        
        if has_components == 's':
            print("\n📝 Ingresa los parámetros (uno por línea, presiona Enter vacío para finalizar):")
            params = []
            while True:
                param = input()
                if not param:
                    break
                params.append(param)
            
            if params:
                # Crear componentes para el template
                # Asumiendo que son parámetros de tipo body
                body_params = [{"type": "text", "text": param} for param in params]
                components = [{
                    "type": "body",
                    "parameters": body_params
                }]
        
        print("\n📤 Enviando mensaje de plantilla...")
        result = sender.send_template_message(
            to=phone,
            template_name=template_name,
            language_code=language_code,
            components=components
        )
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje de plantilla enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar plantilla: {e}")


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python mandar_msg.py [free|template]")
        print("\nEjemplos:")
        print("  python mandar_msg.py free      # Envía un mensaje de texto libre")
        print("  python mandar_msg.py template  # Envía un mensaje usando una plantilla")
        sys.exit(1)
    
    message_type = sys.argv[1].lower()
    
    if message_type == "free":
        send_free_message()
    elif message_type == "template":
        send_template_message()
    else:
        print(f"❌ Tipo de mensaje inválido: {message_type}")
        print("   Usa 'free' o 'template'")
        sys.exit(1)


if __name__ == "__main__":
    main()

