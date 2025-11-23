"""
Script para enviar mensajes de prueba cada 2 segundos
Cada mensaje incluye un número de secuencia para identificarlo
Uso: python cron_test_messages.py [--phone=5693443695]
"""

import sys
import os
import time
import argparse
import signal
from whatsapp_sender import WhatsAppSender
from dotenv import load_dotenv
from datetime import datetime

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# Número de teléfono por defecto
DEFAULT_PHONE = "5693443695"

# Variable global para controlar el loop
running = True


def signal_handler(sig, frame):
    """Maneja la señal de interrupción (Ctrl+C)"""
    global running
    print("\n\n⏹️  Deteniendo envío de mensajes...")
    running = False


def get_phone_number(phone_arg: str = None) -> str:
    """
    Obtiene el número de teléfono desde:
    1. Argumento --phone si se proporciona
    2. Variable de entorno YOUR_PHONE_NUMBER
    3. Valor por defecto DEFAULT_PHONE
    """
    if phone_arg:
        return phone_arg
    
    phone = os.getenv('YOUR_PHONE_NUMBER')
    if phone:
        return phone
    
    return DEFAULT_PHONE


def send_test_message(sender: WhatsAppSender, phone: str, message_number: int):
    """
    Envía un mensaje de prueba con número de secuencia
    """
    try:
        # Crear mensaje con número de secuencia y timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"🧪 Mensaje de prueba #{message_number}\n⏰ Hora: {timestamp}\n📱 Este es el mensaje número {message_number}"
        
        result = sender.send_text_message(phone, message)
        message_id = result.get('messages', [{}])[0].get('id', 'N/A')
        
        print(f"✅ Mensaje #{message_number} enviado - ID: {message_id[:20]}... - Hora: {timestamp}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje #{message_number}: {e}")
        return False


def main():
    """Función principal"""
    global running
    
    parser = argparse.ArgumentParser(
        description='Envía mensajes de prueba cada 2 segundos con número de secuencia',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python cron_test_messages.py                    # Usa teléfono por defecto
  python cron_test_messages.py --phone=123456789  # Usa teléfono específico
  
Presiona Ctrl+C para detener el envío.
        """
    )
    
    parser.add_argument(
        '--phone',
        type=str,
        default=None,
        help=f'Número de teléfono de destino (por defecto: {DEFAULT_PHONE} o YOUR_PHONE_NUMBER del .env)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=2,
        help='Intervalo en segundos entre mensajes (por defecto: 2)'
    )
    
    args = parser.parse_args()
    
    # Configurar manejador de señales para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Obtener número de teléfono
    phone = get_phone_number(args.phone)
    interval = args.interval
    
    print("=" * 60)
    print("🚀 Iniciando envío de mensajes de prueba")
    print("=" * 60)
    print(f"📱 Teléfono de destino: {phone}")
    print(f"⏱️  Intervalo: {interval} segundos")
    print(f"🛑 Presiona Ctrl+C para detener")
    print("=" * 60)
    print()
    
    try:
        # Inicializar el enviador
        sender = WhatsAppSender()
        
        message_number = 1
        
        while running:
            send_test_message(sender, phone, message_number)
            message_number += 1
            
            # Esperar el intervalo especificado (o hasta que se detenga)
            for _ in range(interval):
                if not running:
                    break
                time.sleep(1)
        
        print(f"\n📊 Total de mensajes enviados: {message_number - 1}")
        print("✅ Proceso finalizado")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

