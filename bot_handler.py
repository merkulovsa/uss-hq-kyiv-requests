<<<<<<< HEAD
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
=======
from distutils.command.build import build
import os
import time
import logging
import telegram
import wget
from telegram.error import NetworkError, Unauthorized
from time import sleep
from state_machine import StateMachine, State

TOKEN = None
REQUEST_BUTTON = 'Створити запит'
NUMBER_BUTTON = 'Змінити номер частини'
update_id = None

def get_keyboard_markup(*button_names):
    buttons = [
        [telegram.KeyboardButton(x) for x in button_names]
    ]
    return telegram.ReplyKeyboardMarkup(buttons)

class HandlerState(State):
    def on_bot_update(self, update):
        return

class StartState(HandlerState):
    name = 'StartState'

    def on_bot_update(self, update):
        update.message.reply_text('Hello world!')
        self._next_state = NumberState.name

class NumberState(HandlerState):
    name = 'NumberState'

    def on_bot_update(self, update):
        if update.message.text:
            chat_id = str(update.message.chat.id)
            user_data[chat_id]['number'] = update.message.text

            update.message.reply_text('_number_msg_text', reply_markup=get_keyboard_markup(REQUEST_BUTTON, NUMBER_BUTTON))            

            self._next_state = IdleState.name

class IdleState(HandlerState):
    name = 'IdleState'

    def on_bot_update(self, update):
        if update.message.text == REQUEST_BUTTON:
            self._next_state = RequestState.name
        elif update.message.text == NUMBER_BUTTON:
            self._next_state = NumberState.name

class RequestState(HandlerState):
    name = 'RequestState'

machines = {}
user_data = {}
>>>>>>> sm/dev

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

<<<<<<< HEAD
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
=======
        while True:
            try:
                __process(bot)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                update_id += 1
>>>>>>> sm/dev

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

<<<<<<< HEAD
    updater.start_polling()
=======
def __process(bot):
    global update_id
>>>>>>> sm/dev

    updater.idle()

<<<<<<< HEAD
        
   
=======
        if update.message:
            chat_id = str(update.message.chat.id)

            if chat_id not in machines:
                __init_machine(chat_id)
                user_data[chat_id] = {}

            machines[chat_id].get_active_state().on_bot_update(update)
            machines[chat_id].update()

def __init_machine(chat_id):
    machine = StateMachine()
    machine.add(StartState(machine))
    machine.add(NumberState(machine))
    machine.add(IdleState(machine))
    machine.add(RequestState(machine))

    machine.change(StartState.name)
    
    machines[chat_id] = machine
>>>>>>> sm/dev
