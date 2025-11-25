import os
from whatsapp_sender_v2 import WhatsAppSender
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Número destino, ajústalo si quieres
destino = os.getenv('MARKETING_TEST_PHONE', '56993443695')  # Cambia aquí el número si quieres
TEMPLATE = "appointment_reminder"
PARAMS = ["Osvaldo", "10:00 AM"]     # Primer parámetro: nombre, segundo: fecha/hora
IMAGE_PATH = os.getenv('MARKETING_IMAGE_PATH', '').strip()
IDIOMA = os.getenv('MARKETING_LANG', 'es')


def main():
    sender = WhatsAppSender()
    print(f"Enviando plantilla: {TEMPLATE}")
    print(f"Parámetros: {PARAMS}")
    print(f"Imagen: {IMAGE_PATH if IMAGE_PATH else 'No se enviará imagen'}")
    print(f"Idioma: {IDIOMA}")
    try:
        image_url = None
        if IMAGE_PATH:
            if os.path.exists(IMAGE_PATH):
                print("Subiendo imagen...")
                image_url = sender.upload_media(IMAGE_PATH)
                print(f"URL de la imagen subida: {image_url}")
            else:
                # Si es una url ya pública (http/https)
                if IMAGE_PATH.startswith("http"):
                    image_url = IMAGE_PATH
                else:
                    print(f"No se encontró la imagen local: {IMAGE_PATH}. No se enviará imagen.")
        print(f"Enviando mensaje de marketing a {destino}...")
        # Llamar con o sin la imagen, según corresponda
        if image_url:
            resp = sender.send_marketing_template(
                to=destino,
                template_name=TEMPLATE,
                parameters=PARAMS,
                header_image_url=image_url,
                language_code=IDIOMA,
            )
        else:
            resp = sender.send_marketing_template(
                to=destino,
                template_name=TEMPLATE,
                parameters=PARAMS,
                language_code=IDIOMA,
            )
        print("\nAPI RESPONSE:")
        print(resp)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
