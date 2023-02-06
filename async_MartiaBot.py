from random import choice

import requests
import logging

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5825101258:AAFw08sUikVMv03WheYO8A9Tme6mxlVWf-I'
BOT_NAME = 'CHRNV_Martia_Bot'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def get_martia_price():
    '''The get_martia_price function is an asynchronous function that retrieves the latest prices for Martia using two API calls. The function uses the requests library to make a GET request to the http://wax.alcor.exchange/api/markets/171 API to retrieve the Martia bid price and 24-hour volume. The function also makes a GET request to the https://api.coingecko.com/api/v3/simple/price?ids=wax&vs_currencies=usd API to retrieve the current WAX/USD price.

The function calculates the Martia/USD price by multiplying the WAX/USD price by the Martia bid price. The function then stores the Martia bid price, Martia/USD price, and 24-hour volume in a dictionary with keys 'bid', 'usd', and 'volume24', respectively. Finally, the function returns the dictionary with the Martia price information.'''
    url = 'http://wax.alcor.exchange/api/markets/171'
    wax_url = 'https://api.coingecko.com/api/v3/simple/price?ids=wax&vs_currencies=usd'

    response = requests.get(url).json()
    wax_response = requests.get(wax_url).json()
    wax_price = wax_response.get('wax').get('usd')
    martia_usd = wax_price * response.get('bid')

    martia_info = {'bid': response.get("bid"), 'usd': martia_usd, 'volume24': response.get("volume24")}
    return martia_info


@dp.message_handler(commands='start')
async def handle_start(message: types.Message):
    '''The handle_start function is an asynchronous function that sends a "HELLO!" message to the user when they use the /start command. The function sends the message using the bot.send_message method, where bot is an instance of the bot and message is an instance of the types.Message class from the aiogram library. The chat ID for the message is obtained from the message.chat.id attribute. The message text instructs the user to use the /price command to get the latest Martia price.'''
    await bot.send_message(chat_id=message.chat.id, text='HELLO ! Use /price command to get latest Martia price')


@dp.message_handler(commands='price')
async def send_price(message: types.Message):
    '''The send_price function is an asynchronous function that sends the current prices for Martia when the user uses the /price command. The function uses the get_martia_price function to retrieve the prices for Martia and then rounds the USD price and 24-hour volume to 8 and 2 decimal places, respectively.

The function then selects a greeting from a list of greetings and sends a message to the user's chat with the rounded Martia/WAX price, Martia/USD price, and 24-hour volume. The message is sent using the bot.send_message method, where bot is an instance of the bot and message is an instance of the types.Message class from the aiogram library. The chat ID for the message is obtained from the message.chat.id attribute.'''
    result = await get_martia_price()
    wax = result.get('bid')
    usd = round(result.get('usd'), 8)
    volume = round(result.get('volume24'), 2)
    greetings = ("Here we go, let's take a look.", "Okay, let's examine the results.",
                 "All right, let's see what we have.", "Great, let's check the output.",
                 "Alright, let's take a closer look.", "Okay, let's inspect the findings.",
                 "Let's see what we've got here.", "Sure, let's review the results.",
                 "Let's delve into the data.", "Alright, let's analyze the information.")
    await bot.send_message(chat_id=message.chat.id, text=f'{choice(greetings)}\n'
                                                         f'\n'
                                                         f'Martia/WAX price: {wax}\n'
                                                         f'Martia/USD price: {usd}\n'
                                                         f'Volume24 $: {volume}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
