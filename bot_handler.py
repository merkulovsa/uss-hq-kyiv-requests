from distutils.command.build import build
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import KeyboardButton, ReplyKeyboardMarkup
from time import sleep
from state_machine import StateMachine, State

NEW_LINE = '\n'

TOKEN = None

REQUEST_BUTTON = 'Створити замовлення'
NUMBER_BUTTON = 'Змінити номер частини'
COMPLETE_ORDER_BUTTON = 'Завершити замовлення'
CONFIRM_ORDER_BUTTON = 'Підтвердити замовлення'

update_id = None
order = []

def get_keyboard_markup(*button_names):
    buttons = [
        [KeyboardButton(x) for x in button_names]
    ]
    return ReplyKeyboardMarkup(buttons)

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
            user_data[chat_id]['number'] = update.message.text #why dict of dicts

            update.message.reply_text(
                f'Номер вашої частини: {update.message.text}', 
                reply_markup=get_keyboard_markup(REQUEST_BUTTON, NUMBER_BUTTON)
            )            

            self._next_state = IdleState.name

class IdleState(HandlerState):
    name = 'IdleState'

    def on_bot_update(self, update):
        if update.message.text == REQUEST_BUTTON:
            update.message.reply_text(
                'Створіть ваше замовлення.\nВажливо! Кожне повідомлення - окремий допис.',
                reply_markup=get_keyboard_markup(COMPLETE_ORDER_BUTTON)
            )
            self._next_state = RequestState.name
        elif update.message.text == NUMBER_BUTTON:
            self._next_state = NumberState.name

class RequestState(HandlerState):
    name = 'RequestState'

    def on_bot_update(self, update):
        if update.message.text != COMPLETE_ORDER_BUTTON:
            order.append(str(update.message.text))
            update.message.reply_text(f'Ви додоали до замовлення:\n{update.message.text}')
            print(f'Current order: {order}')
        elif update.message.text == COMPLETE_ORDER_BUTTON:
        

            update.message.reply_text(
                f'Ваше замовлення:{NEW_LINE}{NEW_LINE.join(str(item) for item in order)}',
                reply_markup=get_keyboard_markup(CONFIRM_ORDER_BUTTON)
            )
            
            self._next_state = CompleteOrderState.name


class CompleteOrderState(HandlerState):
    name = 'CompleteOrderState'

    def on_bot_update(self, update):  
        if update.message.text == CONFIRM_ORDER_BUTTON:
            update.message.reply_text('Замовлення підтверджено')
            #further order processing
            #...
            #...
            #...
            self._next_state = IdleState.name

            
machines = {}
user_data = {}

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
    machine.add(CompleteOrderState(machine))

    machine.change(StartState.name)
    
    machines[chat_id] = machine