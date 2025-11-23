# WhatsApp Business API - Testing Tool

Herramienta para testear las funcionalidades de WhatsApp Business API, enfocada en enviar mensajes de tipo **utility** y **service** que son **gratuitos**.

## 📋 Requisitos Previos

1. **Cuenta de Meta for Developers**: Necesitas tener una cuenta en [Meta for Developers](https://developers.facebook.com/)
2. **App de Facebook**: Crea una app en el [Facebook Developer Console](https://developers.facebook.com/apps/)
3. **WhatsApp Business Account**: Configura WhatsApp Business API en tu app
4. **Access Token**: Obtén el token de acceso desde tu app
5. **Phone Number ID**: Obtén el ID del número de teléfono de WhatsApp Business

## 🚀 Instalación

1. **Clonar o descargar este proyecto**

2. **Crear y activar el entorno virtual**:
   
   El proyecto incluye un entorno virtual llamado `crpc_wsp`. Para activarlo:

   **En PowerShell (Windows):**
   ```powershell
   .\crpc_wsp\Scripts\Activate.ps1
   ```
   
   **En CMD (Windows):**
   ```cmd
   crpc_wsp\Scripts\activate.bat
   ```
   
   **En Linux/Mac:**
   ```bash
   source crpc_wsp/bin/activate
   ```
   
   Si el entorno virtual no existe, créalo primero:
   ```bash
   python -m venv crpc_wsp
   ```

3. **Instalar dependencias**:
   
   Con el entorno virtual activado:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar credenciales**:
   - Copia el archivo `env_template.txt` y renómbralo a `.env`
   - Completa las credenciales en el archivo `.env`:
   ```
   WHATSAPP_ACCESS_TOKEN=tu_token_aqui
   WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
   YOUR_PHONE_NUMBER=tu_numero_personal_aqui
   WHATSAPP_API_VERSION=v21.0
   ```

## 📝 Formato del Número de Teléfono

El número debe estar en formato internacional **sin** el símbolo `+` ni espacios:
- ✅ Correcto: `5491123456789` (Argentina)
- ✅ Correcto: `5215512345678` (México)
- ❌ Incorrecto: `+54 9 11 1234-5678`
- ❌ Incorrecto: `+5491123456789`

## 💰 Tipos de Mensajes Gratuitos

Este proyecto está configurado para enviar mensajes **gratuitos** de dos tipos:

### 1. **Utility** (Utilidad)
- Confirmaciones de transacciones
- Recordatorios de citas
- Notificaciones de estado
- Actualizaciones de pedidos

### 2. **Service** (Servicio)
- Mensajes de atención al cliente
- Soporte técnico
- Actualizaciones de servicio
- Respuestas a consultas

## 🎯 Uso

⚠️ **Importante**: Antes de ejecutar cualquier script, asegúrate de tener el entorno virtual activado.

### Activar el entorno virtual:

**PowerShell:**
```powershell
.\crpc_wsp\Scripts\Activate.ps1
```

**CMD:**
```cmd
crpc_wsp\Scripts\activate.bat
```

### Verificar configuración:
```bash
python check_config.py
```

Este script verifica que todas las credenciales estén configuradas correctamente.

### Ejecutar el script principal:
```bash
python whatsapp_sender.py
```

Este script enviará automáticamente:
- Un mensaje de tipo **utility**
- Un mensaje de tipo **service**

### Ejemplos adicionales:
```bash
python test_examples.py
```

### Usar como módulo:

```python
from whatsapp_sender import WhatsAppSender

# Inicializar
sender = WhatsAppSender()

# Enviar mensaje de utilidad
sender.send_utility_message(
    to="5491123456789",
    message="Tu pedido ha sido confirmado. ID: #12345"
)

# Enviar mensaje de servicio
sender.send_service_message(
    to="5491123456789",
    message="Gracias por contactarnos. Estamos aquí para ayudarte."
)
```

## 📁 Estructura del Proyecto

```
test_whatsapp/
├── crpc_wsp/            # Entorno virtual (no se sube a git)
├── whatsapp_sender.py   # Script principal con la clase WhatsAppSender
├── test_examples.py     # Ejemplos adicionales de uso
├── check_config.py      # Script para verificar configuración
├── requirements.txt     # Dependencias del proyecto
├── env_template.txt     # Plantilla para archivo .env
├── .gitignore          # Archivos a ignorar en git
└── README.md           # Este archivo
```

## 🔒 Seguridad

- ⚠️ **NUNCA** subas el archivo `.env` a un repositorio público
- El archivo `.env` está incluido en `.gitignore` para proteger tus credenciales
- Mantén tus credenciales seguras y no las compartas

## 🐛 Solución de Problemas

### Error: "Faltan credenciales"
- Verifica que el archivo `.env` existe y contiene todas las variables necesarias
- Asegúrate de que no hay espacios extra en las credenciales
- Ejecuta `python check_config.py` para verificar tu configuración

### Error: "ModuleNotFoundError" o "No module named 'requests'"
- Asegúrate de tener el entorno virtual activado
- Verifica que instalaste las dependencias: `pip install -r requirements.txt`
- Si el entorno virtual no existe, créalo: `python -m venv crpc_wsp`

### Error: "Invalid OAuth access token"
- Verifica que tu Access Token es válido y no ha expirado
- Regenera el token si es necesario desde el Facebook Developer Console

### Error: "Invalid phone number"
- Verifica que el número está en formato correcto (sin +, sin espacios)
- Asegúrate de que el número incluye el código de país

### Error: "Message type not allowed"
- Verifica que estás usando los tipos correctos: `utility` o `service`
- Algunos tipos de mensajes requieren aprobación previa de Meta

## 📚 Recursos Adicionales

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers](https://developers.facebook.com/)
- [WhatsApp Business API Pricing](https://developers.facebook.com/docs/whatsapp/pricing)

## 📄 Licencia

Este proyecto es para uso de testing y validación de costos.

