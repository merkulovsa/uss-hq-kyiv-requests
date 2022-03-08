import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import KeyboardButton, ReplyKeyboardMarkup
from time import sleep
from state_machine import StateMachine, State

NEW_LINE = '\n'

REQUEST_BUTTON = 'Створити замовлення'
NUMBER_BUTTON = 'Змінити номер частини'
COMPLETE_ORDER_BUTTON = 'Завершити замовлення'
CONFIRM_ORDER_BUTTON = 'Підтвердити замовлення'
CANCEL_ORDER_BUTTON = 'Скасувати замовлення'

update_id = None
bot = None
machines = {}
chat_ids = {}
user_datas = {}

class HandlerState(State):
    def get_chat_id(self):
        return chat_ids[self._state_machine]

    def get_user_data(self):
        return user_datas[self.get_chat_id()]

    def on_bot_update(self, update):
        pass

    def send_message(self, text, *button_names):
        global bot

        buttons = [
            [KeyboardButton(x) for x in button_names]
        ]
        bot.send_message(chat_id=self.get_chat_id(), text=text, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


class StartState(HandlerState):
    name = 'StartState'

    def on_bot_update(self, update):
        self._next_state = NumberState.name

class NumberState(HandlerState):
    name = 'NumberState'

    def enter(self):
        super().enter()

        self.send_message('Введіть номер частини:')

    def on_bot_update(self, update):
        if update.message.text:
            self.get_user_data()['number'] = update.message.text
            self._next_state = IdleState.name

class IdleState(HandlerState):
    name = 'IdleState'

    def enter(self):
        super().enter()

        number = self.get_user_data()['number']

        self.send_message(f'Номер вашої частини: {number}')
        self.send_message('Виберіть наступний крок:', REQUEST_BUTTON, NUMBER_BUTTON)

    def on_bot_update(self, update):
        if update.message.text == REQUEST_BUTTON:
            self._next_state = RequestState.name
        elif update.message.text == NUMBER_BUTTON:
            self._next_state = NumberState.name

class RequestState(HandlerState):
    name = 'RequestState'

    def enter(self):
        super().enter()

        self.get_user_data()['order'] = []
        self.send_message('Створіть ваше замовлення.\nВажливо! Кожне повідомлення - окремий допис.', COMPLETE_ORDER_BUTTON)

    def on_bot_update(self, update):
        if update.message.text != COMPLETE_ORDER_BUTTON:
            self.get_user_data()['order'].append(str(update.message.text))
            self.send_message(f'Ви додали до замовлення:\n{update.message.text}', COMPLETE_ORDER_BUTTON)
            
        elif update.message.text == COMPLETE_ORDER_BUTTON:
            self._next_state = CompleteOrderState.name


class CompleteOrderState(HandlerState):
    name = 'CompleteOrderState'

    def enter(self):
        super().enter()

        order = self.get_user_data()['order']

        self.send_message(f'Ваше замовлення:{NEW_LINE}{NEW_LINE.join(str(item) for item in order)}', CONFIRM_ORDER_BUTTON, CANCEL_ORDER_BUTTON)

    def on_bot_update(self, update):  
        if update.message.text == CONFIRM_ORDER_BUTTON:
            self.send_message('Замовлення підтверджено')
            #further order processing
            #...
            #...
            #...
        elif update.message.text == CANCEL_ORDER_BUTTON:
            self.send_message('Замовлення скасовано')
        
        self._next_state = IdleState.name

def start():
    global update_id
    global bot

    with open('TOKEN', 'r') as f:
        token = f.read()
        bot = telegram.Bot(token)

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
                user_datas[chat_id] = {}

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
    chat_ids[machine] = chat_id