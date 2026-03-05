import telebot
import os
from dotenv import load_dotenv  

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(['start', 'help'])
def start(msg:telebot.types.Message):
    bot.reply_to(msg, 'Olá, sou o bot gotinha a sua disposição!')


bot.infinity_polling()
