import requests
import time
import os
import os
from dotenv import load_dotenv
import telebot

TOKEN = os.getenv('token')
BOT_NAME = 'CHRNV_Martia_Bot'
CHRNV
bot = telebot.TeleBot(TOKEN)

def get_martia_price():
    # Используйте API Alcorexchange, чтобы получить текущий курс токена Martia
    url = 'http://wax.alcor.exchange/api/markets/171'

    response = requests.get(url).json()

    return response.get('bid')

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'HELLO ! Use /price command to get latest Martia price')


@bot.message_handler(commands=['price'])
def send_price(message):
    price = get_martia_price()
    bot.send_message(message.chat.id, f'Current Martia/WAX price: {price}')

while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        time.sleep(15)
