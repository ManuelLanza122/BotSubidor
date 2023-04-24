from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
import stripe
import os
import requests
from telegram import Update

from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')

updater = Updater(api_id = API_ID, api_hash = API_HASH, use_context = True)

# Configuración de la clave secreta de Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Función para descargar un archivo
def download(update: Update, context):
if update.effective_user.username == ADMIN_USERNAME:
# Si el usuario es un administrador, descargar el archivo
# Replace FILE_URL with your file URL
file_url = "FILE_URL"
file_name = "my_file.mp4"
response = requests.get(file_url, stream = True)
with open(file_name, 'wb') as f:
for chunk in response.iter_content(chunk_size = 1024):
if chunk:
f.write(chunk)
update.message.reply_text("Archivo descargado exitosamente.")
else :
# Si el usuario no es un administrador, responder con un mensaje de error
update.message.reply_text("Lo siento, solo los administradores tienen permiso para descargar archivos.")

# Función para generar un enlace de pago
def generar_enlace_de_pago(cantidad, descripcion):
# Crear un objeto de pago en Stripe
pago = stripe.PaymentIntent.create(
    amount = cantidad,
    currency = "usd",
    description = descripcion
)

# Devolver el enlace de pago generado por Stripe
return pago['charges']['data'][0]['receipt_url']

# Función para verificar si un usuario tiene permiso para descargar contenido
def verificar_permiso_de_descarga(update):
# Verificar si el usuario es un administrador
if update.effective_user.username == ADMIN_USERNAME:
return True

# Si el usuario no es un administrador, generar un enlace de pago
enlace_de_pago = generar_enlace_de_pago(100, "Descarga de contenido")
update.message.reply_text("Para descargar este contenido, debe realizar un pago de $100 USD. Haga clic en este enlace para realizar el pago: " + enlace_de_pago)
return False

def main():
updater = Updater(token = TOKEN, use_context = True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('download', download))

updater.start_polling()
updater.idle()

if __name__ == '__main__':
main()