"""
Script simple para probar el envío de templates de utilidad
Uso: python test_template.py [template_name] [--phone=5693443695]
"""

import sys
import os
import argparse
from whatsapp_sender import WhatsAppSender
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# Número de teléfono por defecto
DEFAULT_PHONE = "5693443695"


def get_phone_number(phone_arg: str = None) -> str:
    """Obtiene el número de teléfono"""
    if phone_arg:
        return phone_arg
    
    phone = os.getenv('YOUR_PHONE_NUMBER')
    if phone:
        return phone
    
    return DEFAULT_PHONE


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Prueba el envío de templates de utilidad',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python test_template.py mi_plantilla                    # Prueba plantilla sin parámetros
  python test_template.py mi_plantilla --phone=123456789  # Con número específico
  python test_template.py mi_plantilla --params param1 param2  # Con parámetros
        """
    )
    
    parser.add_argument(
        'template_name',
        type=str,
        help='Nombre de la plantilla a probar'
    )
    
    parser.add_argument(
        '--phone',
        type=str,
        default=None,
        help=f'Número de teléfono de destino (por defecto: {DEFAULT_PHONE})'
    )
    
    parser.add_argument(
        '--params',
        nargs='*',
        default=None,
        help='Parámetros para la plantilla (opcional)'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        default='es',
        help='Código de idioma (por defecto: es)'
    )
    
    args = parser.parse_args()
    
    # Obtener número de teléfono
    phone = get_phone_number(args.phone)
    
    print("=" * 60)
    print("🧪 Test de Template de Utilidad")
    print("=" * 60)
    print(f"📱 Teléfono de destino: {phone}")
    print(f"📋 Plantilla: {args.template_name}")
    print(f"🌐 Idioma: {args.lang}")
    if args.params:
        print(f"📝 Parámetros: {args.params}")
    else:
        print(f"📝 Parámetros: None")
    print("=" * 60)
    print()
    
    try:
        sender = WhatsAppSender()
        
        print("📤 Enviando template...")
        result = sender.send_utility_message(
            to=phone,
            template_name=args.template_name,
            parameters=args.params,
            language_code=args.lang
        )
        
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print("✅ Template enviado exitosamente!")
        print(f"   Message ID: {message_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


