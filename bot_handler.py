import os
import time
import logging
import telegram
import wget
from telegram.error import NetworkError, Unauthorized
from time import sleep

TOKEN = None
update_id = None
handlers = {}


def start():
    global update_id

    with open('TOKEN', 'r') as f:
        TOKEN = f.read()
        bot = telegram.Bot(TOKEN)

        try:
            update_id = bot.get_updates()[0].update_id
        except IndexError:
            update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        while True:
            try:
                __process(bot)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                update_id += 1


def __process(bot):
    global update_id

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:
            if update.message.text in handlers:
                handlers[update.message.text](update)

def __start_command(update):
    buttons = [
        [
            telegram.KeyboardButton('Створити запит')
        ]
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)

    update.message.reply_text('Hello world!', reply_markup=reply_markup)

def __request_command(update):
    update.message.reply_text('Request received!')

handlers['/start'] = __start_command
handlers['Створити запит'] = __request_command
