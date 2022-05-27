import telebot
from telebot import types


class BaseState:
    text = ''
    sticker = ''
    status = ''
    anime_id = ''
    id = ''

    def __init__(self, bot: telebot.TeleBot, chat_id, msg_to_del=None):
        self.bot = bot
        self.chat_id = chat_id
        self.msg_to_del = msg_to_del

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def display(self):
        sent = []
        if self.sticker:
            if self.text:
                sent.append(self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker))
            else:
                sent.append(
                    self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker, reply_markup=self.get_keyboard()))
        if self.msg_to_del:
            for msg_id in self.msg_to_del:
                self.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
        if self.text:
            sent.append(
                self.bot.send_message(self.chat_id, self.text, reply_markup=self.get_keyboard(), parse_mode='html'))
        return sent

    def get_msg_text(self):
        return self.text

    def get_keyboard(self):
        return None

    def send_warning(self, text):
        self.bot.send_message(self.chat_id, text, reply_markup=self.get_keyboard(), parse_mode='html')

    def send_anime(self, result):
        html_text = f'''
        
<b>TITLE: </b>{result["title"]}

        '''
        self.bot.send_photo(self.chat_id, result["url_img"], caption=html_text, parse_mode='html', reply_markup=None)

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        return self.__class__(self.bot, self.chat_id)

    def process_text_message(self, message: types.Message) -> 'BaseState':
        return self.__class__(self.bot, self.chat_id)

    def delete_msg_text(self, msg_id):
        msg_id_list = [msg.message_id for msg in msg_id]
        print(msg_id_list)
        self.msg_to_del = msg_id_list

