#import os
#import time
import logging
#import telegram
#import wget
#from telegram.error import NetworkError, Unauthorized
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
#from time import sleep


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start_command(update: Update, context: CallbackContext):
    buttons = [
        [
            KeyboardButton('Створити замовлення'),
            KeyboardButton('Кнопка 3')
        ]
    ]

    reply_markup=ReplyKeyboardMarkup(buttons)
    
    update.message.reply_text('_start_msg_text', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
            '_help_comm_text'
        )

def message_handler(update: Update, context: CallbackContext):
     update.message.reply_text(
         update.message.text
         )

     print(f'privet merku na servere, msg text: {update.message.text}')

def very_start():
    with open('TOKEN', 'r') as f:
        TOKEN = f.read()

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()

    updater.idle()

        
   