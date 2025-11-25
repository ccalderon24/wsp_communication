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
from pathlib import Path
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
        self.waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')  # Opcional, para listar plantillas
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
        parameters: List[str] = None,
        language_code: str = "es"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje usando una plantilla UTILITY (notificaciones).
        Si no se proporcionan parámetros, envía la plantilla sin componentes.
        """
        components = None
        
        if parameters:
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
    # 📤 SUBIR IMAGEN A WHATSAPP MEDIA API
    # ===============================
    def upload_media(self, file_path: str, media_type: str = "image") -> str:
        """
        Sube una imagen a la API de Media de WhatsApp y retorna la URL.
        
        Args:
            file_path: Ruta local del archivo de imagen
            media_type: Tipo de medio ('image', 'document', etc.)
        
        Returns:
            URL de la imagen subida
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        
        media_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/media"
        
        try:
            with open(file_path, 'rb') as file:
                files = {
                    'file': (os.path.basename(file_path), file, f'image/{file_path.split(".")[-1]}')
                }
                data = {
                    'messaging_product': 'whatsapp',
                    'type': media_type
                }
                headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }
                
                response = requests.post(
                    media_url,
                    headers=headers,
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                
                # Obtener el media_id
                media_id = result.get('id')
                if not media_id:
                    raise Exception("No se recibió un media_id de la API")
                
                # Obtener la URL de la imagen desde el media_id
                media_info_url = f"https://graph.facebook.com/{self.api_version}/{media_id}"
                info_response = requests.get(
                    media_info_url,
                    headers=headers
                )
                info_response.raise_for_status()
                media_info = info_response.json()
                
                # La URL puede estar en diferentes campos según la API
                url = media_info.get('url') or media_info.get('link')
                if url:
                    return url
                
                # Para plantillas, WhatsApp requiere URLs públicas accesibles
                # Si no obtenemos una URL directa, intentamos usar el formato de descarga
                # Nota: Esto puede no funcionar para plantillas, puede requerir un servicio de hosting
                download_url = f"https://graph.facebook.com/{self.api_version}/{media_id}"
                
                # Intentar verificar si la URL es accesible
                try:
                    test_response = requests.head(download_url, headers=headers, timeout=5)
                    if test_response.status_code == 200:
                        return download_url
                except:
                    pass
                
                # Si no funciona, lanzar error explicativo
                raise Exception(
                    f"La imagen se subió (media_id: {media_id}), pero WhatsApp requiere una URL pública "
                    "para usar en plantillas. Considera subir la imagen a un servicio de hosting "
                    "de imágenes (como imgur, cloudinary, etc.) y usar esa URL."
                )
                
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Error subiendo imagen: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.json()
                    error_msg += f"\nDetalles: {detail}"
                except:
                    error_msg += f"\nStatus Code: {e.response.status_code}"
            raise Exception(error_msg)

    # ===============================
    # 📋 LISTAR PLANTILLAS DISPONIBLES
    # ===============================
    def list_templates(self) -> Dict[str, Any]:
        """
        Lista todas las plantillas disponibles en tu cuenta de WhatsApp Business.
        Requiere el WhatsApp Business Account ID (WABA ID) en la variable de entorno
        WHATSAPP_BUSINESS_ACCOUNT_ID, o se intentará obtenerlo automáticamente.
        """
        waba_id = self.waba_id
        
        # Si no está en .env, intentar obtenerlo desde el access token
        if not waba_id:
            try:
                # Obtener información del usuario/app para encontrar el WABA ID
                me_url = f"https://graph.facebook.com/{self.api_version}/me"
                response = requests.get(
                    me_url,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                # Intentar obtener WABA desde el access token (puede requerir permisos adicionales)
                # Si esto no funciona, el usuario debe agregar WHATSAPP_BUSINESS_ACCOUNT_ID al .env
                raise Exception(
                    "No se encontró WHATSAPP_BUSINESS_ACCOUNT_ID en .env. "
                    "Agrega esta variable con tu WABA ID. "
                    "Puedes encontrarlo en Meta Business Manager > Configuración de WhatsApp > Configuración de API"
                )
            except requests.exceptions.RequestException:
                raise Exception(
                    "No se encontró WHATSAPP_BUSINESS_ACCOUNT_ID en .env. "
                    "Agrega esta variable con tu WABA ID."
                )
        
        # Listar plantillas
        try:
            templates_url = f"https://graph.facebook.com/{self.api_version}/{waba_id}/message_templates"
            response = requests.get(
                templates_url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Error listando plantillas: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.json()
                    error_msg += f"\nDetalles: {detail}"
                except:
                    error_msg += f"\nStatus Code: {e.response.status_code}"
            raise Exception(error_msg)

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
