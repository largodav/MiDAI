#Utilziando pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI)
import os
import telebot 
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()
tokenbot = os.getenv("BOT_KEY")

# Verificar si el token se cargó correctamente
if not tokenbot:
    raise ValueError("Error: La clave BOT_KEY no está definida en el archivo .env o no se está cargando correctamente.")
else:
    print(f"Token cargado correctamente")


#Creamos el bot...
bot = telebot.TeleBot(tokenbot,parse_mode=None) 

#Definamos un controlador de mensajes que maneje los comandos entrantes /start y /help.
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,"Hola, primer mensaje")
    
#Este método envía todos los mensajes de texto entrantes al remitente. Utiliza una función 
# lambda para probar un mensaje. Si la lambda devuelve "True", la función decorada
# gestiona el mensaje. Como queremos que esta función gestione todos los mensajes, 
# simplemente devolvemos "True"
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    bot.reply_to(message,message.text)
    
#Ahora tenemos un bot básico que responde con un mensaje estático a los comandos "/start" y "/help" y que replica el resto de los mensajes enviados. Para iniciar el bot, agregue lo siguiente a nuestro archivo fuente:
bot.infinity_polling()

