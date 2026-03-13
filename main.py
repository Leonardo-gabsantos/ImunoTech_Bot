import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_inicio = types.KeyboardButton('Início')
    btn_vacinas = types.KeyboardButton('Vacinas')
    btn_help = types.KeyboardButton('Help')
    markup.add(btn_inicio, btn_vacinas, btn_help)

    bot.send_message(msg.chat.id, 'Olá, sou o bot Gotinha! Clique no botão abaixo para começar.', reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Início")
def resposta_inicio(msg):
    bot.reply_to(msg, "Você voltou ao início! Como posso te ajudar?")

# --- ALTERAÇÃO AQUI: SOLICITA A IDADE ---
@bot.message_handler(func=lambda msg: msg.text == "Vacinas")
def pedir_idade(msg):
    # Enviamos a pergunta e dizemos qual função deve processar a resposta
    sent_msg = bot.reply_to(msg, "Para saber as informações sobre as vacinas, digite apenas o número da sua idade da pessoa que você quer saber as informações:")
    bot.register_next_step_handler(sent_msg, processar_idade)

# --- NOVA FUNÇÃO: PROCESSA E DESIGNA A FAIXA ETÁRIA ---
def processar_idade(msg):
    idade_texto = msg.text
    
    if not idade_texto.isdigit():
        sent_msg = bot.reply_to(msg, "Por favor, digite apenas números (ex: 25). Tente clicar em 'Vacinas' novamente.")
        return

    idade = int(idade_texto)
    faixa_etaria = ""

    # Lógica de categorização
    if idade < 1:
        faixa_etaria = "Recém-nascidos e Bebês (0 a 11 meses)"
    elif 1 <= idade <= 12:
        faixa_etaria = "Criança"
    elif 13 <= idade <= 17:
        faixa_etaria = "Adolescente"
    elif 18 <= idade <= 59:
        faixa_etaria = "Adulto"
    else:
        faixa_etaria = "Idoso"

    # Aqui você já tem a variável 'faixa_etaria' pronta para a raspagem futura
    bot.reply_to(msg, f"Identifiquei que a pessoa se enquadra como: {faixa_etaria}.\n\n"
                      "Em breve, trarei as vacinas específicas para você via raspagem de dados!")

@bot.message_handler(func=lambda msg: msg.text == "Help")
def resposta_help(msg):
    bot.reply_to(msg, "Como posso te ajudar?")

bot.infinity_polling()