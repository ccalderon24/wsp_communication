"""
Script para verificar que la configuración esté correcta
"""

import os
from dotenv import load_dotenv

load_dotenv()


def check_config():
    """Verifica que todas las variables de entorno estén configuradas"""
    print("🔍 Verificando configuración...\n")
    
    required_vars = {
        'WHATSAPP_ACCESS_TOKEN': 'Token de acceso de WhatsApp',
        'WHATSAPP_PHONE_NUMBER_ID': 'ID del número de teléfono',
        'YOUR_PHONE_NUMBER': 'Tu número personal'
    }
    
    optional_vars = {
        'WHATSAPP_API_VERSION': 'Versión de la API (opcional)'
    }
    
    all_ok = True
    
    print("📋 Variables requeridas:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            # Mostrar solo los primeros y últimos caracteres por seguridad
            masked = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            print(f"  ✅ {var}: {masked} ({description})")
        else:
            print(f"  ❌ {var}: NO CONFIGURADO ({description})")
            all_ok = False
    
    print("\n📋 Variables opcionales:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value} ({description})")
        else:
            print(f"  ⚠️  {var}: No configurado, se usará el valor por defecto ({description})")
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ ¡Configuración correcta! Puedes ejecutar whatsapp_sender.py")
    else:
        print("❌ Faltan variables de configuración")
        print("\n💡 Pasos a seguir:")
        print("   1. Copia env_template.txt y renómbralo a .env")
        print("   2. Completa todas las variables requeridas en .env")
        print("   3. Vuelve a ejecutar este script para verificar")
    
    return all_ok


if __name__ == "__main__":
    check_config()

