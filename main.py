import telebot
import os
from dotenv import load_dotenv
from telebot import types # Import necessário para os botões

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    
    btn_inicio = types.KeyboardButton('Início')
    
    
    markup.add(btn_inicio)
    
    bot.send_message(msg.chat.id, 'Olá, sou o bot gotinha a sua disposição! Clique no botão abaixo para começar.', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == "Início")
def resposta_inicio(msg):
    bot.reply_to(msg, "Você voltou ao início! Como posso te ajudar com as vacinas hoje?")

bot.infinity_polling()