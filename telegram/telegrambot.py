import os
import telebot

from telegram.states.base import BaseState
from telegram.states.start import Start

from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
clients: dict = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot_new = Start(bot, message.chat.id)
    bot_new.display()
    clients[message.chat.id] = Start(bot,message.chat.id)


@bot.callback_query_handler(func=lambda message: True)
def process_call_back(message):
    chat_id = message.from_user.id
    new_state_class = get_state(chat_id).process_call_back(message)
    clients[chat_id] = new_state_class
    display(chat_id)



@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    chat_id = message.chat.id
    new_state_class = get_state(chat_id).process_text_message(message)
    clients[chat_id] = new_state_class
    display(chat_id)


def display(chat_id):
    state = get_state(chat_id)
    prev_msg = state.display()
    state.delete_msg_text(msg_id=prev_msg)



def get_state(chat_id) -> BaseState:
    examples_of_class = clients.get(chat_id, Start(bot, chat_id))
    return examples_of_class


