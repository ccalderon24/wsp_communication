"""
WhatsApp Business API - Enviador de Mensajes
Envía mensajes de tipo 'utility' y 'service' (gratuitos)
"""

import os
import sys
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()


class WhatsAppSender:
    """Clase para enviar mensajes a través de WhatsApp Business API"""
    
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.api_version = os.getenv('WHATSAPP_API_VERSION', 'v21.0')
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        
        if not self.access_token or not self.phone_number_id:
            raise ValueError(
                "Faltan credenciales. Asegúrate de configurar WHATSAPP_ACCESS_TOKEN "
                "y WHATSAPP_PHONE_NUMBER_ID en el archivo .env"
            )
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna los headers necesarios para las peticiones"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _format_phone_number(self, phone: str) -> str:
        """
        Formatea el número de teléfono al formato requerido por WhatsApp
        Elimina espacios, guiones y el símbolo +
        """
        return phone.replace(' ', '').replace('-', '').replace('+', '')
    
    def send_text_message(
        self, 
        to: str, 
        message: str,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje de texto
        
        Nota: Los mensajes de texto son GRATUITOS si están dentro de la ventana de 24 horas
        desde la última interacción del usuario. El parámetro message_type se mantiene por
        compatibilidad pero NO se usa en el payload (siempre se envía como "text").
        
        IMPORTANTE: Para enviar mensajes de utilidad/servicio como templates (fuera de ventana de 24h),
        usa send_template_message() con una plantilla aprobada de tipo utility o service.
        
        Args:
            to: Número de teléfono del destinatario (formato: código_país + número)
            message: Contenido del mensaje
            message_type: Parámetro mantenido por compatibilidad (no se usa en la API)
        
        Returns:
            Respuesta de la API de WhatsApp
        """
        formatted_phone = self._format_phone_number(to)
        
        # Los mensajes de texto simples SIEMPRE deben tener type: "text"
        # Los tipos "utility" y "service" solo aplican a templates
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": formatted_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        # Nota: Los mensajes de texto simples son gratuitos si están dentro de la ventana de 24 horas
        # desde la última interacción del usuario. Los tipos "utility" y "service" se aplican
        # principalmente a plantillas (templates) para mensajes fuera de la ventana de 24 horas.
        
        try:
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Error al enviar mensaje: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f"\nDetalles: {error_detail}"
                except:
                    error_msg += f"\nStatus: {e.response.status_code}"
            raise Exception(error_msg)
    
    def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "es",
        components: Optional[list] = None,
        message_type: str = "utility"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje usando una plantilla pre-aprobada
        
        Args:
            to: Número de teléfono del destinatario
            template_name: Nombre de la plantilla aprobada
            language_code: Código de idioma (por defecto 'es')
            components: Componentes de la plantilla (parámetros)
            message_type: Tipo de mensaje ('utility' o 'service')
        
        Returns:
            Respuesta de la API de WhatsApp
        """
        formatted_phone = self._format_phone_number(to)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": formatted_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        # Nota: El tipo de mensaje (utility/service) se especifica al crear la plantilla
        # en el Meta Business Manager, no en el payload de envío.
        
        try:
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Error al enviar plantilla: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f"\nDetalles: {error_detail}"
                except:
                    error_msg += f"\nStatus: {e.response.status_code}"
            raise Exception(error_msg)
    
    def send_utility_message(
        self, 
        to: str, 
        template_name: str,
        parameters: list = None,
        language_code: str = "es"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje usando una plantilla de tipo UTILITY (template)
        
        IMPORTANTE: Este método envía un TEMPLATE de utilidad, NO un mensaje de texto simple.
        Los templates de utilidad se usan para mensajes fuera de la ventana de 24 horas
        y pueden incurrir en costos según la tarifa de WhatsApp Business API.
        
        Args:
            to: Número de teléfono del destinatario
            template_name: Nombre de la plantilla aprobada de tipo "utility"
            parameters: Lista de parámetros para la plantilla (opcional)
            language_code: Código de idioma (por defecto 'es')
        
        Returns:
            Respuesta de la API de WhatsApp
        
        Ejemplo:
            sender.send_utility_message(
                to="5693443695",
                template_name="order_confirmation",
                parameters=["Jessica", "SKBUP2-4CPIG9"],
                language_code="es"
            )
        """
        return self.send_utility_template(
            to=to,
            template_name=template_name,
            parameters=parameters,
            language_code=language_code
        )
    
    def send_service_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Envía un mensaje de texto simple (gratuito dentro de ventana de 24 horas)
        Útil para mensajes de servicio al cliente, soporte, etc.
        
        IMPORTANTE: Este método envía un mensaje de texto simple (type: "text"), NO un template.
        Es gratuito SOLO si el usuario ha interactuado contigo en las últimas 24 horas.
        
        Para enviar mensajes de servicio como TEMPLATES (fuera de ventana de 24h), usa:
        send_template_message() con una plantilla aprobada de tipo "service".
        """
        return self.send_text_message(to, message)
    
    def send_utility_template(
        self,
        to: str,
        template_name: str,
        parameters: list = None,
        language_code: str = "es"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje usando una plantilla de tipo UTILITY (fuera de ventana de 24 horas)
        
        Args:
            to: Número de teléfono del destinatario
            template_name: Nombre de la plantilla aprobada de tipo "utility"
            parameters: Lista de parámetros para la plantilla (opcional)
            language_code: Código de idioma (por defecto 'es')
        
        Returns:
            Respuesta de la API de WhatsApp
        
        Ejemplo:
            sender.send_utility_template(
                to="5693443695",
                template_name="order_confirmation",
                parameters=["Jessica", "SKBUP2-4CPIG9"],
                language_code="es"
            )
        """
        components = None
        if parameters:
            components = [{
                "type": "body",
                "parameters": [
                    {"type": "text", "text": param} for param in parameters
                ]
            }]
        
        return self.send_template_message(
            to=to,
            template_name=template_name,
            language_code=language_code,
            components=components
        )
    
    def send_service_template(
        self,
        to: str,
        template_name: str,
        parameters: list = None,
        language_code: str = "es"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje usando una plantilla de tipo SERVICE (fuera de ventana de 24 horas)
        
        Args:
            to: Número de teléfono del destinatario
            template_name: Nombre de la plantilla aprobada de tipo "service"
            parameters: Lista de parámetros para la plantilla (opcional)
            language_code: Código de idioma (por defecto 'es')
        
        Returns:
            Respuesta de la API de WhatsApp
        """
        components = None
        if parameters:
            components = [{
                "type": "body",
                "parameters": [
                    {"type": "text", "text": param} for param in parameters
                ]
            }]
        
        return self.send_template_message(
            to=to,
            template_name=template_name,
            language_code=language_code,
            components=components
        )


def main():
    """Función principal para testing"""
    try:
        # Inicializar el enviador
        sender = WhatsAppSender()
        
        # Obtener número personal desde variables de entorno
        your_phone = os.getenv('YOUR_PHONE_NUMBER')
        if not your_phone:
            print("⚠️  No se encontró YOUR_PHONE_NUMBER en .env")
            your_phone = input("Ingresa tu número de teléfono (código_país + número): ")
        
        print("\n🚀 WhatsApp Business API - Testing\n")
        print("=" * 50)
        
        # Ejemplo 1: Mensaje de utilidad (template)
        print("\n📤 Enviando mensaje de UTILIDAD (template)...")
        print("   Usando plantilla 'hello_world' (template por defecto de Meta)")
        
        message_ids = []
        
        try:
            # Enviar template de utilidad usando hello_world (sin parámetros)
            result = sender.send_utility_message(
                to=your_phone,
                template_name="hello_world",
                parameters=None,  # hello_world no requiere parámetros
                language_code="es"
            )
            message_id = result.get('messages', [{}])[0].get('id', 'N/A')
            message_ids.append(message_id)
            print("✅ Mensaje de utilidad (template) enviado exitosamente!")
            print(f"   Message ID: {message_id}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Ejemplo 2: Mensaje de servicio
        print("\n📤 Enviando mensaje de SERVICIO...")
        service_message = "🛎️ Este es un mensaje de prueba de tipo SERVICIO. " \
                         "Este tipo de mensaje es gratuito y se usa para atención al cliente, " \
                         "soporte técnico, actualizaciones de servicio, etc."
        
        try:
            result = sender.send_service_message(your_phone, service_message)
            message_id = result.get('messages', [{}])[0].get('id', 'N/A')
            message_ids.append(message_id)
            print("✅ Mensaje de servicio enviado exitosamente!")
            print(f"   Message ID: {message_id}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)
        print("✨ Testing completado!")
        
        # Mostrar información importante si los mensajes se enviaron
        if message_ids:
            print("\n" + "=" * 50)
            print("📱 IMPORTANTE: Si no recibiste los mensajes")
            print("=" * 50)
            print("\n⚠️  Para recibir mensajes en WhatsApp Business API:")
            print("\n1. Tu número debe estar agregado como 'Número de Prueba' en Meta")
            print("   Pasos:")
            print("   a) Ve a: https://developers.facebook.com/apps/")
            print("   b) Selecciona tu app")
            print("   c) Ve a: WhatsApp → API Setup")
            print("   d) En 'To', haz clic en 'Manage phone number list'")
            print("   e) Agrega tu número: +" + your_phone)
            print("\n2. O el número debe haber iniciado una conversación contigo")
            print("   en las últimas 24 horas (ventana de mensajes gratuitos)")
            print("\n💡 Para verificar el estado de los mensajes:")
            print("   python check_message_status.py")
            print("=" * 50)
        
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 Asegúrate de:")
        print("   1. Crear un archivo .env basado en .env.example")
        print("   2. Configurar todas las credenciales necesarias")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()

