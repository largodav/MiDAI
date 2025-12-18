#Utilziando pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI)
import os
import telebot 

tokenbot = os.getenv("BOT_KEY")

#Creamos el bot...
bot = telebot.TeleBot('8517090768:AAEMGQ-42KDfY2yVan2RFeLMICq23icxYNM',parse_mode=None) 

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

