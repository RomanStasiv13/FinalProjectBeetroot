import telebot
from telebot import types


class BaseState:
    text = ''
    sticker = ''
    status = ''
    anime_id = ''

    def __init__(self, bot: telebot.TeleBot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def display(self):
        if self.sticker:
            if self.text:
                self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker)
            else:
                self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker, reply_markup=self.get_keyboard())
        if self.text:
            self.bot.send_message(self.chat_id, self.text, reply_markup=self.get_keyboard(), parse_mode='html')

    def get_keyboard(self):
        return None

    def send_warning(self, text):
        self.bot.send_message(self.chat_id, text, reply_markup=self.get_keyboard(), parse_mode='html')

    def send_anime(self, result):
        html_text = f'''
        
<b>TITLE: </b>{result["title"]}

        '''
        self.bot.send_photo(self.chat_id, result["url_img"], caption=html_text, parse_mode='html')

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        return self.__class__(self.bot, self.chat_id)

    def process_text_message(self, message: types.Message) -> 'BaseState':
        return self.__class__(self.bot, self.chat_id)

