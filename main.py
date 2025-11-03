import os
import telebot
from dotenv import load_dotenv
import requests
from telebot import types
import json


load_dotenv()

# Get Telegram bot token from .env file
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

# Global variable for the amount entered by the user
amount = 0


# --- Function: Search for a coin ID using CoinGecko's /search endpoint ---
def search_coin_id(query):
    url = 'https://api.coingecko.com/api/v3/search'
    params = {'query': query}
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            coins = data.get('coins', [])
            if coins:
                # Return the ID of the first matching coin (best match)
                return coins[0].get('id')
        return None
    except Exception as e:
        print(f"Error searching for coin: {e}")
        return None


# --- Function: Get real-time crypto price in USD ---
def get_crypto_price(coin_id):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': coin_id.lower(),
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Return the price if it exists, otherwise None
            return data.get(coin_id.lower(), {}).get('usd', None)
        return None
    except Exception as e:
        print(f"Error fetching CoinGecko data: {e}")
        return None


# --- Start command handler ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Enter an amount in USD, and I will show you how much it is in your selected cryptocurrency.'
    )
    bot.register_next_step_handler(message, summa)


# --- Function: Get the amount in USD from the user ---
def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid format. Please enter a valid number.')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        # Create buttons for popular cryptocurrencies
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('BTC', callback_data='bitcoin')
        btn2 = types.InlineKeyboardButton('ETH', callback_data='ethereum')
        btn3 = types.InlineKeyboardButton('BNB', callback_data='binancecoin')
        btn4 = types.InlineKeyboardButton('Other', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, 'Choose a cryptocurrency:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'The amount must be greater than 0. Try again.')
        bot.register_next_step_handler(message, summa)
        return


# --- Callback handler for button clicks ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        # If user chose one of the predefined coins
        price = get_crypto_price(call.data)

        if price:
            total = amount / price
            bot.send_message(
                call.message.chat.id,
                f'{amount} USD = {round(total, 4)} {call.data.upper()} '
                f'(at a rate of {round(price, 4)} USD per 1 {call.data.upper()})'
            )
            bot.send_message(call.message.chat.id, 'Enter a new amount in USD or choose another coin.')
            bot.register_next_step_handler(call.message, summa)
            return
        else:
            bot.send_message(call.message.chat.id, 'Error retrieving price. Try again.')
            bot.register_next_step_handler(call.message, summa)
            return

    else:
        # If user selected "Other" currency
        bot.send_message(call.message.chat.id, 'Enter the name or ticker of the cryptocurrency:')
        bot.register_next_step_handler(call.message, my_currency)
        return


# --- Function: Handle user input for a custom coin ---
def my_currency(message):
    user_input = message.text.strip().lower()
    coin_id = user_input

    # Try to find the correct coin ID using /search
    found_id = search_coin_id(user_input)
    if found_id:
        coin_id = found_id

    # Fetch the real-time price
    price = get_crypto_price(coin_id)
    if price:
        total = amount / price
        bot.send_message(
            message.chat.id,
            f'{amount} USD = {round(total, 4)} {coin_id.upper()} '
            f'(at a rate of {round(price, 4)} USD per 1 {coin_id.upper()})'
        )
        bot.send_message(message.chat.id, 'Enter a new amount in USD or choose another coin.')
        bot.register_next_step_handler(message, summa)
        return
    else:
        bot.send_message(message.chat.id, 'Could not find this coin. Please try again.')
        bot.register_next_step_handler(message, my_currency)
        return



bot.polling(none_stop=True)
