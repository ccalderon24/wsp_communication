"""
Script para listar todas las plantillas de WhatsApp disponibles
Uso: python list_templates.py
"""

import sys
import json
from whatsapp_sender_v2 import WhatsAppSender
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()


def main():
    """Función principal"""
    try:
        sender = WhatsAppSender()
        
        print("\n📋 Obteniendo plantillas disponibles...\n")
        result = sender.list_templates()
        
        templates = result.get('data', [])
        
        if not templates:
            print("❌ No se encontraron plantillas.")
            return
        
        print(f"✅ Se encontraron {len(templates)} plantilla(s):\n")
        print("=" * 80)
        
        for i, template in enumerate(templates, 1):
            name = template.get('name', 'N/A')
            status = template.get('status', 'N/A')
            category = template.get('category', 'N/A')
            language = template.get('language', 'N/A')
            
            print(f"\n{i}. Nombre: {name}")
            print(f"   Estado: {status}")
            print(f"   Categoría: {category}")
            print(f"   Idioma: {language}")
            
            # Mostrar componentes si existen
            components = template.get('components', [])
            if components:
                print(f"   Componentes:")
                for comp in components:
                    comp_type = comp.get('type', 'N/A')
                    if comp_type == 'body':
                        text = comp.get('text', 'N/A')
                        print(f"     - Tipo: {comp_type}, Texto: {text[:50]}...")
                    elif comp_type == 'header':
                        format_type = comp.get('format', 'N/A')
                        print(f"     - Tipo: {comp_type}, Formato: {format_type}")
                    else:
                        print(f"     - Tipo: {comp_type}")
        
        print("\n" + "=" * 80)
        print("\n💡 Para usar una plantilla, copia el nombre exacto y úsalo en mandar_msg_v2.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()


