"""
Script para enviar mensajes de WhatsApp desde la terminal (v2)
Uso: python mandar_msg_v2.py [free|template|auth|utility|marketing] [--phone=5693443695]
"""

import sys
import os
import argparse
from whatsapp_sender_v2 import WhatsAppSender
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# Número de teléfono por defecto
DEFAULT_PHONE = "5693443695"

# Valores hardcoded para plantillas
DEFAULT_AUTH_TEMPLATE = "nombre_plantilla_auth"  # Cambiar por el nombre real de tu plantilla
DEFAULT_AUTH_CODE = "123456"  # Código OTP por defecto
DEFAULT_UTILITY_TEMPLATE = "nombre_plantilla_utility"  # Cambiar por el nombre real
DEFAULT_UTILITY_PARAMS = ["param1", "param2"]  # Parámetros por defecto
DEFAULT_MARKETING_TEMPLATE = "nombre_plantilla_marketing"  # Cambiar por el nombre real
DEFAULT_MARKETING_PARAMS = ["param1", "param2"]  # Parámetros por defecto
DEFAULT_MARKETING_IMAGE_URL = None  # URL de imagen por defecto (None si no hay)
DEFAULT_LANGUAGE_CODE = "es"  # Código de idioma por defecto


def get_phone_number(phone_arg: str = None) -> str:
    """
    Obtiene el número de teléfono desde:
    1. Argumento --phone si se proporciona
    2. Variable de entorno YOUR_PHONE_NUMBER
    3. Valor por defecto DEFAULT_PHONE
    4. Input del usuario si nada está disponible
    """
    if phone_arg:
        return phone_arg
    
    phone = os.getenv('YOUR_PHONE_NUMBER')
    if phone:
        return phone
    
    return DEFAULT_PHONE


def send_free_message(phone: str):
    """Envía un mensaje de texto libre (free)"""
    try:
        sender = WhatsAppSender()
        
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
        
        print(f"\n📤 Enviando mensaje libre a {phone}...")
        result = sender.send_text_message(phone, message)
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")


def send_template_message(phone: str):
    """Envía un mensaje usando una plantilla (template)"""
    try:
        sender = WhatsAppSender()
        
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
        
        print(f"\n📤 Enviando mensaje de plantilla a {phone}...")
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


def send_authentication_message(phone: str):
    """Envía un mensaje de autenticación (OTP/código)"""
    try:
        sender = WhatsAppSender()
        
        # Valores hardcoded
        template_name = DEFAULT_AUTH_TEMPLATE
        code = DEFAULT_AUTH_CODE
        language_code = DEFAULT_LANGUAGE_CODE
        
        print(f"\n📋 Plantilla: {template_name}")
        print(f"🔐 Código OTP: {code}")
        print(f"🌐 Idioma: {language_code}")
        print(f"\n📤 Enviando mensaje de autenticación a {phone}...")
        
        result = sender.send_authentication_template(
            to=phone,
            template_name=template_name,
            code=code,
            language_code=language_code
        )
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje de autenticación enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje de autenticación: {e}")


def send_utility_message(phone: str):
    """Envía un mensaje de utilidad (notificaciones)"""
    try:
        sender = WhatsAppSender()
        
        # Valores hardcoded
        template_name = DEFAULT_UTILITY_TEMPLATE
        params = DEFAULT_UTILITY_PARAMS.copy()
        language_code = DEFAULT_LANGUAGE_CODE
        
        print(f"\n📋 Plantilla: {template_name}")
        print(f"📝 Parámetros: {params}")
        print(f"🌐 Idioma: {language_code}")
        print(f"\n📤 Enviando mensaje de utilidad a {phone}...")
        
        result = sender.send_utility_template(
            to=phone,
            template_name=template_name,
            parameters=params,
            language_code=language_code
        )
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje de utilidad enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje de utilidad: {e}")


def send_marketing_message(phone: str):
    """Envía un mensaje de marketing (promociones/ofertas)"""
    try:
        sender = WhatsAppSender()
        
        # Valores hardcoded
        template_name = DEFAULT_MARKETING_TEMPLATE
        params = DEFAULT_MARKETING_PARAMS.copy()
        header_image_url = DEFAULT_MARKETING_IMAGE_URL
        language_code = DEFAULT_LANGUAGE_CODE
        
        print(f"\n📋 Plantilla: {template_name}")
        print(f"📝 Parámetros: {params}")
        if header_image_url:
            print(f"🖼️  Imagen header: {header_image_url}")
        else:
            print("🖼️  Imagen header: No")
        print(f"🌐 Idioma: {language_code}")
        print(f"\n📤 Enviando mensaje de marketing a {phone}...")
        
        result = sender.send_marketing_template(
            to=phone,
            template_name=template_name,
            parameters=params,
            header_image_url=header_image_url,
            language_code=language_code
        )
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Mensaje de marketing enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje de marketing: {e}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Envía mensajes de WhatsApp desde la terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python mandar_msg_v2.py free                    # Envía un mensaje libre (usa teléfono por defecto)
  python mandar_msg_v2.py free --phone=123456789   # Envía un mensaje libre a número específico
  python mandar_msg_v2.py template                # Envía un mensaje de plantilla genérica
  python mandar_msg_v2.py auth                    # Envía un mensaje de autenticación (OTP)
  python mandar_msg_v2.py utility                 # Envía un mensaje de utilidad (notificaciones)
  python mandar_msg_v2.py marketing                # Envía un mensaje de marketing (promociones)
  python mandar_msg_v2.py marketing --phone=987654321  # Con número específico
        """
    )
    
    parser.add_argument(
        'tipo',
        choices=['free', 'template', 'auth', 'utility', 'marketing'],
        help='Tipo de mensaje: "free" (texto libre), "template" (genérico), "auth" (autenticación), "utility" (utilidad), "marketing" (marketing)'
    )
    
    parser.add_argument(
        '--phone',
        type=str,
        default=None,
        help=f'Número de teléfono de destino (por defecto: {DEFAULT_PHONE} o YOUR_PHONE_NUMBER del .env)'
    )
    
    args = parser.parse_args()
    
    # Obtener número de teléfono
    phone = get_phone_number(args.phone)
    print(f"📱 Teléfono de destino: {phone}")
    
    # Enviar mensaje según el tipo
    if args.tipo == "free":
        send_free_message(phone)
    elif args.tipo == "template":
        send_template_message(phone)
    elif args.tipo == "auth":
        send_authentication_message(phone)
    elif args.tipo == "utility":
        send_utility_message(phone)
    elif args.tipo == "marketing":
        send_marketing_message(phone)


if __name__ == "__main__":
    main()

