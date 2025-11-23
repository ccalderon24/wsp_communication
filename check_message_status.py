"""
Script para verificar el estado de los mensajes enviados
"""

import os
import sys
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()


def check_message_status(message_id: str) -> Dict[str, Any]:
    """
    Verifica el estado de un mensaje enviado
    
    Args:
        message_id: ID del mensaje (wamid.xxx)
    
    Returns:
        Estado del mensaje
    """
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    api_version = os.getenv('WHATSAPP_API_VERSION', 'v21.0')
    
    if not access_token:
        raise ValueError("WHATSAPP_ACCESS_TOKEN no configurado")
    
    url = f"https://graph.facebook.com/{api_version}/{message_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al verificar mensaje: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f"\nDetalles: {error_detail}"
            except:
                error_msg += f"\nStatus: {e.response.status_code}"
        raise Exception(error_msg)


def verify_phone_number(phone_number: str) -> None:
    """
    Muestra información sobre cómo verificar/agregar un número de teléfono
    """
    print("\n" + "=" * 60)
    print("📱 INFORMACIÓN IMPORTANTE SOBRE NÚMEROS DE PRUEBA")
    print("=" * 60)
    print(f"\nNúmero configurado: {phone_number}")
    print("\n⚠️  Para recibir mensajes en WhatsApp Business API:")
    print("\n1. El número debe estar agregado como 'Número de Prueba' en Meta")
    print("2. Pasos para agregar tu número:")
    print("   a) Ve a: https://developers.facebook.com/apps/")
    print("   b) Selecciona tu app")
    print("   c) Ve a: WhatsApp → API Setup")
    print("   d) En la sección 'To', haz clic en 'Manage phone number list'")
    print("   e) Agrega tu número de teléfono (formato: +[código_país][número])")
    print("   f) Ejemplo: +5491123456789")
    print("\n3. Alternativamente, el número debe haber iniciado una conversación")
    print("   contigo en las últimas 24 horas (ventana de mensajes gratuitos)")
    print("\n" + "=" * 60)


def main():
    """Función principal"""
    print("🔍 Verificador de Estado de Mensajes de WhatsApp\n")
    
    # Verificar número configurado
    phone = os.getenv('YOUR_PHONE_NUMBER')
    if phone:
        verify_phone_number(phone)
    
    # Solicitar Message ID si se quiere verificar
    print("\n" + "=" * 60)
    print("¿Quieres verificar el estado de un mensaje específico?")
    print("Pega el Message ID (wamid.xxx) o presiona Enter para salir")
    message_id = input("\nMessage ID: ").strip()
    
    if not message_id:
        print("\n👋 Saliendo...")
        return
    
    if not message_id.startswith('wamid.'):
        print("⚠️  El Message ID debe comenzar con 'wamid.'")
        return
    
    try:
        print(f"\n🔍 Verificando mensaje: {message_id}...")
        status = check_message_status(message_id)
        
        print("\n✅ Estado del mensaje:")
        print("-" * 60)
        for key, value in status.items():
            print(f"  {key}: {value}")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

