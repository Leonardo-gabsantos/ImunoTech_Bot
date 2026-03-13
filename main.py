import telebot
import os
from datetime import datetime
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

@bot.message_handler(func=lambda msg: msg.text == "Vacinas")
def pedir_data_nascimento(msg):
    # Aqui, pede a data de nascimento
    sent_msg = bot.reply_to(msg, "Para verificar as vacinas recomendadas, informe a data de nascimento da pessoa no formato DD/MM/AAAA.")
    bot.register_next_step_handler(sent_msg, processar_data)

def processar_data(msg):
    data_texto = msg.text
    
    try:
        #converter o texto para um objeto de data
        data_nascimento = datetime.strptime(data_texto, "%d/%m/%Y")
        hoje = datetime.now()
        
        #calcular a idade
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

        if idade < 0:
            bot.reply_to(msg, "A data de nascimento não pode ser no futuro! Tente novamente clicando em 'Vacinas'.")
            return

        
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

        bot.reply_to(msg, f"Data confirmada com sucesso! ✅ \n\nA pessoa tem {idade} anos e pertence ao grupo: {faixa_etaria}.\n"
                          f"Vou listar as vacinas recomendadas para esta faixa etária em São José dos Campos\n\n"
                          f"⌛Aguarde um instante enquanto eu busco as informações...")
                          
    except ValueError:
        
        bot.reply_to(msg, "Formato de data inválido! Por favor, use o padrão **DD/MM/AAAA**. Clique em 'Vacinas' para tentar de novo.")

@bot.message_handler(func=lambda msg: msg.text == "Help")
def resposta_help(msg):
    bot.reply_to(msg, "Como posso te ajudar?")

bot.infinity_polling()