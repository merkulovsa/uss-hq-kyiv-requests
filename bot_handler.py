import os
import time
import logging
import telegram
import wget
from telegram.error import NetworkError, Unauthorized
from time import sleep

TOKEN = None
update_id = None


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
                process(bot)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                update_id += 1


def process(bot):
    global update_id

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:
            print(update.message.text)
