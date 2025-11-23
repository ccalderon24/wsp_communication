"""
WhatsApp Business API - Enviador de Mensajes (Categorías Oficiales)
Autor: César Calderón
Versión: 2.0

Incluye envío de:
- Mensajes de texto gratuitos dentro de ventana de servicio (24h)
- Plantillas AUTHENTICATION
- Plantillas UTILITY
- Plantillas MARKETING
- Plantillas SERVICE
"""

import os
import sys
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar variables de entorno desde el .env
load_dotenv()


class WhatsAppSender:
    """Clase principal para enviar mensajes mediante WhatsApp Business API."""

    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.api_version = os.getenv('WHATSAPP_API_VERSION', 'v21.0')

        if not self.access_token or not self.phone_number_id:
            raise ValueError(
                "Faltan credenciales. Configura WHATSAPP_ACCESS_TOKEN y WHATSAPP_PHONE_NUMBER_ID en .env"
            )

        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    def _get_headers(self) -> Dict[str, str]:
        """Headers de autorización."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def _format_phone_number(self, phone: str) -> str:
        """Normaliza el número al formato internacional requerido por Meta."""
        return phone.replace(' ', '').replace('-', '').replace('+', '')

    # ===============================
    # 📌 MENSAJES DE TEXTO (24H)
    # ===============================
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Envía un mensaje de texto gratuito mientras estés dentro de la ventana de 24 horas.
        """
        formatted_phone = self._format_phone_number(to)

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

        return self._post(payload)

    # ===============================
    # 📌 ENVÍO GENÉRICO DE PLANTILLAS
    # ===============================
    def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "es",
        components: Optional[List] = None
    ) -> Dict[str, Any]:

        formatted_phone = self._format_phone_number(to)

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": formatted_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }

        if components:
            payload["template"]["components"] = components

        return self._post(payload)

    # ===============================
    # 🔒 1. AUTENTICATION (OTP / MFA)
    # ===============================
    def send_authentication_template(
        self,
        to: str,
        template_name: str,
        code: str,
        language_code: str = "es"
    ) -> Dict[str, Any]:
        """
        Enviar un OTP/código de autenticación usando plantillas AUTHENTICATION.
        """

        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": code}
                ]
            }
        ]

        return self.send_template_message(
            to,
            template_name,
            language_code,
            components
        )

    # ===============================
    # 🏷️ 2. UTILITY (Notificaciones)
    # ===============================
    def send_utility_template(
        self,
        to: str,
        template_name: str,
        parameters: List[str],
        language_code: str = "es"
    ) -> Dict[str, Any]:

        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": p} for p in parameters
                ]
            }
        ]

        return self.send_template_message(
            to,
            template_name,
            language_code,
            components
        )

    # ===============================
    # 📣 3. MARKETING (Promos / Ofertas)
    # ===============================
    def send_marketing_template(
        self,
        to: str,
        template_name: str,
        parameters: List[str],
        header_image_url: Optional[str] = None,
        language_code: str = "es"
    ) -> Dict[str, Any]:

        components = []

        if header_image_url:
            components.append({
                "type": "header",
                "parameters": [
                    {"type": "image", "image": {"link": header_image_url}}
                ]
            })

        components.append({
            "type": "body",
            "parameters": [
                {"type": "text", "text": p} for p in parameters
            ]
        })

        return self.send_template_message(
            to,
            template_name,
            language_code,
            components
        )

    # ===============================
    # 🛎️ 4. SERVICE (Plantillas de soporte)
    # ===============================
    def send_service_template(
        self,
        to: str,
        template_name: str,
        parameters: List[str],
        language_code: str = "es"
    ) -> Dict[str, Any]:

        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": p} for p in parameters
                ]
            }
        ]

        return self.send_template_message(
            to,
            template_name,
            language_code,
            components
        )

    # ===============================
    # 📌 FUNCIÓN PRIVADA PARA PETICIONES
    # ===============================
    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la petición POST y errores."""
        try:
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Error enviando mensaje: {str(e)}"

            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.json()
                    error_msg += f"\nDetalles: {detail}"
                except:
                    error_msg += f"\nStatus Code: {e.response.status_code}"

            raise Exception(error_msg)
