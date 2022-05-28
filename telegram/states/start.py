import random
import requests
from telebot import types
from telegram.states.base import BaseState
import os
from dotenv import load_dotenv

load_dotenv()


class Start(BaseState):
    text = "<b>Hello,my Lord! I'm here to recommend you a title and remember all titles you've watched or plan to watch.</b>"
    sticker = 'CAACAgIAAxkBAAEUKNdihhm7pq-GNVsRfrZWEix3MCLL_wACKgADOPBYCAUt1BilRArHJAQ'

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'nextstate:ShowMenu':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
        return Start(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        menu = types.InlineKeyboardButton('Order',
                                          callback_data='nextstate:ShowMenu')
        markup.add(menu)
        return markup


class ShowMenu(BaseState):
    text = "<b>Please, tell me what to do, Master!</b>"
    sticker = "CAACAgIAAxkBAAEUKNtihhnwf8S39U7fo8mGKlmwfhyDCAACBwADOPBYCMnWVk19q0b4JAQ"

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'nextstate:Search':
                return Search(self.bot, self.chat_id, self.msg_to_del)
            if message.data == 'nextstate:Random':
                return Random(self.bot, self.chat_id, self.msg_to_del)
            if message.data == 'nextstate:MyLists':
                ml = MyLists(self.bot, self.chat_id, self.msg_to_del)
                return ml
        return ShowMenu(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        search_button = types.InlineKeyboardButton('Search title 🔎',
                                                   callback_data='nextstate:Search')
        random_button = types.InlineKeyboardButton('Random title 🎲',
                                                   callback_data='nextstate:Random')
        my_list_button = types.InlineKeyboardButton('My list 📜',
                                                    callback_data='nextstate:MyLists')
        markup.add(search_button, random_button, my_list_button)
        return markup


class Search(BaseState):
    text = "<b>How should I search, Master?</b>"
    sticker = "CAACAgIAAxkBAAEUOQ1iiJSi3cMIzAABD9b0lMNCHQaqsB0AAgsAAzjwWAiOC45uDqDEDiQE"

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
            ml = SearchBy(self.bot, self.chat_id, self.msg_to_del)
            ml.status = message.data
            return ml
        return Search(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        search_by_name = types.InlineKeyboardButton('Search by name 🖋',
                                                    callback_data='title')
        search_by_genre = types.InlineKeyboardButton('Search by genre 🎭',
                                                     callback_data='genres')
        search_by_studio = types.InlineKeyboardButton('Search by studio 🎬',
                                                      callback_data='studio')
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(search_by_name, search_by_genre, search_by_studio, back_button)
        print(markup)
        return markup


class Random(BaseState):
    text = "<b>Here your random title!</b>"
    sticker = "CAACAgIAAxkBAAEUOVFiiKHIExWgZMtFr-y0nJpjFtKmJQACSAADOPBYCAe1nGGTQPbPJAQ"

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data[:9] == 'nextstate':
                add_to_list = AddToList(self.bot, self.chat_id, self.msg_to_del)
                add_to_list.anime_id = str(message.data[9:])
                return add_to_list
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
            if message.data == 'repeat':
                return Random(self.bot, self.chat_id, self.msg_to_del)
            a_d = AnimeDetails(self.bot, self.chat_id, self.msg_to_del)
            a_d.anime_id = message.data
            return a_d
        return Random(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        r = requests.get('http://127.0.0.1:8000/api/animebase/?format=json&limit=1')
        data = r.json()
        randomizer = random.randrange(1, data['count'])
        r = requests.get(f'http://127.0.0.1:8000/api/animebase/?format=json&limit=1&offset={randomizer}')
        anime = r.json()
        self.send_anime(anime['results'][0])

        markup = types.InlineKeyboardMarkup(row_width=2)
        add_button = types.InlineKeyboardButton('Add to list ⭐',
                                                callback_data='nextstate' + str(anime['results'][0]['id_a']))
        detail_button = types.InlineKeyboardButton('Detail 👁‍🗨', callback_data=anime['results'][0]['id_a'])
        next_rand_button = types.InlineKeyboardButton('Next ➡', callback_data='repeat')
        back_button = types.InlineKeyboardButton('Back ↩', callback_data='prevstate')
        markup.add(add_button, detail_button, back_button, next_rand_button)
        return markup


class MyLists(BaseState):
    text = f"<b>Your bee...Oh, I mean your lists, Master!</b>"
    sticker = "CAACAgIAAxkBAAEUOYJiiKwaSlG-ud2mGJ14ndSpX4UFDwACNgADOPBYCLeuZtFoIia4JAQ"

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data == 'prevstate':
            return ShowMenu(self.bot, self.chat_id, self.msg_to_del)

        ml = Lists(self.bot, self.chat_id, self.msg_to_del)
        ml.status = message.data
        return ml

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        watching = types.InlineKeyboardButton('Watching 👀',
                                              callback_data='watching')
        completed = types.InlineKeyboardButton('Completed ✅',
                                               callback_data='completed')
        on_hold = types.InlineKeyboardButton('On Hold 🕓',
                                             callback_data='on_hold')
        dropped = types.InlineKeyboardButton('Dropped 🗑',
                                             callback_data='dropped')
        ptw = types.InlineKeyboardButton('Plan to watch 📝',
                                         callback_data='plan_to_watch')
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(watching, completed, on_hold, dropped, ptw, back_button)
        return markup


class SearchBy(BaseState):
    text = "-"
    status = '-'

    def display(self):
        sent = []
        if self.text == "-":
            self.text = f"<b>Please enter the parameter!</b>"
            sent.append(self.bot.send_message(self.chat_id, self.text, parse_mode='html'))
        return sent

    def process_text_message(self, message: types.Message) -> 'BaseState':
        if message.text:
            r = requests.get(f'http://127.0.0.1:8000/api/animebase/?format=json&{self.status}={message.text}')
            anime = r.json()
            if anime['results'] != []:
                for i in range(len(anime['results'])):
                    self.send_anime(anime['results'][i])
                    self.bot.send_message(self.chat_id, '<b>Would you like to add this title?</b>',
                                          reply_markup=self.add_to_list(anime['results'][i]['id_a']), parse_mode='html')

                return self
            else:
                self.bot.send_sticker(self.chat_id,
                                      "CAACAgIAAxkBAAEUOcViiLi6QVKH8GYyoJ8e1Cth1Hx0bAACDwADOPBYCCxiVtQnXxReJAQ")
                self.bot.send_message(self.chat_id,
                                      "<b>There is no such anime</b>",
                                      reply_markup=self.get_keyboard(),
                                      parse_mode='html')
            return Search(self.bot, self.chat_id, self.msg_to_del)

    def add_to_list(self, id_a):
        markup = types.InlineKeyboardMarkup(row_width=2, )
        detail_button = types.InlineKeyboardButton('Detail 👁‍🗨', callback_data=id_a)
        add_to_list = types.InlineKeyboardButton('Add to list ⭐', callback_data='nextstate' + str(id_a))
        markup.add(add_to_list, detail_button)
        return markup

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data[:9] == 'nextstate':
                add_to_list = AddToList(self.bot, self.chat_id, self.msg_to_del)
                add_to_list.anime_id = str(message.data[9:])
                return add_to_list
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
            a_d = AnimeDetails(self.bot, self.chat_id, self.msg_to_del)
            a_d.anime_id = message.data
            return a_d

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(back_button)
        return markup


class Lists(BaseState):  # Подивитися списки
    text = f"<b>Here is your list!</b>"
    sticker = "CAACAgIAAxkBAAEUbndikNf-8LUfI3yZBlxCpEGlHUbY5AACTgADOPBYCJzN1qooiz_HJAQ"

    def get_lists(self):
        r = requests.get(f"http://127.0.0.1:8000/api/subscribers?chat_id={self.chat_id}&status={self.status}")
        return r.json()

    def display(self):
        sent = []
        if self.sticker:
            if self.text:
                self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker)
            else:
                self.bot.send_sticker(chat_id=self.chat_id, sticker=self.sticker, reply_markup=self.get_keyboard())
        if self.msg_to_del:
            for msg_id in self.msg_to_del:
                self.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
        if self.text:
            sent.append(
                self.bot.send_message(self.chat_id, self.text, reply_markup=self.get_keyboard(), parse_mode='html'))
        return sent

    def send_anime(self, result):
        html_text = f'''
        <b>title</b>:{result['title']}
'''
        if result['year']:
            html_text += f"<b>year: </b>{result['year']}\n"
        if result['score']:
            html_text += f"<b>score: </b>{result['score']}\n"
        if result['status']:
            html_text += f"<b>status: </b>{result['status']}\n"
        self.bot.send_message(self.chat_id, html_text, parse_mode='html',
                              reply_markup=self.move_keybord(result['id_a']))

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data[:6] == 'moveto':
                move = MoveToMyLists(self.bot, self.chat_id, self.msg_to_del)
                move.id = self.get_sub(message.data[6:])
                return move
            if message.data[:6] == 'remove':
                self.remove_item(message.data[6:])
                self.bot.send_message(self.chat_id, "<b>The title was successfully removed.</b>", parse_mode='html')
                return MyLists(self.bot, self.chat_id, self.msg_to_del)
            if message.data == 'prevstate':
                return MyLists(self.bot, self.chat_id, self.msg_to_del)

    def remove_item(self, id_a):
        r = requests.delete(f'http://127.0.0.1:8000/api/subscribers/{self.get_sub(id_a)}/',
                            auth=(os.getenv('USER'), os.getenv('PASSWORD')))

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        anime_id = self.get_lists()
        for i in range(len(anime_id['results'])):
            r = requests.get(f"http://127.0.0.1:8000/api/animebase/{anime_id['results'][i]['anime_id']}")
            anime_title = r.json()
            self.send_anime(anime_title)
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(back_button)
        return markup

    def get_sub(self, id_a):
        r = requests.get(
            f'http://127.0.0.1:8000/api/subscribers?chat_id={self.chat_id}&status={self.status}&anime_id={id_a}')
        item = r.json()
        return item["results"][0]["id_u"]

    def move_keybord(self, id_a):
        markup = types.InlineKeyboardMarkup(row_width=2, )
        remove_button = types.InlineKeyboardButton('Remove ❌',
                                                   callback_data='remove' + str(id_a))
        move_button = types.InlineKeyboardButton('Move to ↘',
                                                 callback_data='moveto' + str(id_a))
        markup.add(remove_button, move_button)
        return markup


class AddToList(BaseState):  # Додати до списку
    text = 'Please choose the list you wanna add to.'

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
            done = ViewDoneAdd(self.bot, self.chat_id, self.msg_to_del)
            done.anime_id = self.anime_id
            done.status = message.data
            return done
        return AddToList(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        watching = types.InlineKeyboardButton('Watching 👀',
                                              callback_data='watching')
        completed = types.InlineKeyboardButton('Completed ✅',
                                               callback_data='completed')
        on_hold = types.InlineKeyboardButton('On Hold 🕓',
                                             callback_data='on_hold')
        dropped = types.InlineKeyboardButton('Dropped 🗑',
                                             callback_data='dropped')
        ptw = types.InlineKeyboardButton('Plan to watch 📝',
                                         callback_data='plan_to_watch')
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(watching, completed, on_hold, dropped, ptw, back_button)
        return markup


class EndState(BaseState):
    sticker = 'CAACAgIAAxkBAAEUUcRijN2Ydj62TDWZl9PZwt4-XT-LAQACFgADOPBYCG2PHd_3dhKoJAQ'

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(back_button)
        return markup


class AnimeDetails(BaseState):
    sticker = "CAACAgIAAxkBAAEUUcRijN2Ydj62TDWZl9PZwt4-XT-LAQACFgADOPBYCG2PHd_3dhKoJAQ"

    def send_anime(self, result):
        html_text = ""
        if result['title_eng']:
            html_text += f"<b>english title: </b>{result['title_eng']}\n"
        if result['title_jap']:
            html_text += f"<b>japanese title: </b>{result['title_jap']}\n"
        if result['description']:
            html_text += f"<b>description: </b>{result['description']}\n"
        if result['year']:
            html_text += f"<b>year: </b>{result['year']}\n"
        if result['score']:
            html_text += f"<b>score: </b>{result['score']}\n"
        if result['episodes']:
            html_text += f"<b>episodes: </b>{result['episodes']}\n"
        if result['rating']:
            html_text += f"<b>age rating: </b>{result['rating']}\n"
        if result['status']:
            html_text += f"<b>status: </b>{result['status']}\n"
        if result['id_s']:
            r = requests.get(f'http://127.0.0.1:8000/api/studios/{result["id_s"]}')
            html_text += f"<b>studio: </b>{(r.json())['title']}\n"
        if result['genres']:
            genres_title = ""
            for g in range(len(result['genres'])):
                r = requests.get(f'http://127.0.0.1:8000/api/genres/{result["genres"][g]}')
                genres_title += (r.json())['title'] + "  "
            html_text += f"<b>genres: </b>{genres_title}\n"
        if result['demographics_genres']:
            demo_genres_title = ""
            for g in range(len(result['demographics_genres'])):
                r = requests.get(f'http://127.0.0.1:8000/api/genres/{result["demographics_genres"][g]}')
                demo_genres_title += (r.json())['title'] + "  "
            html_text += f"<b>demographic genres: </b>{demo_genres_title}\n"
        if result['themes']:
            themes_title = ""
            for g in range(len(result['themes'])):
                r = requests.get(f'http://127.0.0.1:8000/api/genres/{result["themes"][g]}')
                themes_title += (r.json())['title'] + "  "
            html_text += f"<b>themes: </b>{themes_title}\n"
        if result['explicit_genres']:
            exp_genres_title = ""
            for g in range(len(result['explicit_genres'])):
                r = requests.get(f'http://127.0.0.1:8000/api/genres/{result["explicit_genres"][g]}')
                exp_genres_title += (r.json())['title'] + "  "
            html_text += f"<b>explicit_genres: </b>{exp_genres_title}\n"
        if result['trailer_url']:
            html_text += f"<b>trailer: </b>{result['trailer_url']}\n"
        self.bot.send_photo(self.chat_id, result["url_img"], caption=result['title'], parse_mode='html')
        self.bot.send_message(self.chat_id, html_text, parse_mode='html')

    def get_keyboard(self):
        r = requests.get(f'http://127.0.0.1:8000/api/animebase/{self.anime_id}')
        anime = r.json()
        self.send_anime(anime)

        markup = types.InlineKeyboardMarkup(row_width=2)
        add_button = types.InlineKeyboardButton('Add to list ⭐', callback_data='nextstate' + str(self.anime_id))
        back_button = types.InlineKeyboardButton('Back ↩', callback_data='prevstate')
        markup.add(add_button, back_button)
        return markup

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data[:9] == 'nextstate':
                add_to_list = AddToList(self.bot, self.chat_id, self.msg_to_del)
                add_to_list.anime_id = str(message.data[9:])
                return add_to_list
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)
        return AnimeDetails(self.bot, self.chat_id, self.msg_to_del)


class ViewDoneAdd(BaseState):
    text = '<b>Your anime was add!</b>'
    sticker = "CAACAgIAAxkBAAEUYu5ij3lStXwVwsJ3exgOwPXeWSHhjgACIgADOPBYCIu4GMWylYdDJAQ"

    def add_to_list(self):
        data = {
            "chat_id": self.chat_id,
            "status": self.status,
            "anime_id": self.anime_id
        }
        r = requests.post('http://127.0.0.1:8000/api/subscribers/', data=data,
                          auth=(os.getenv('USER'), os.getenv('PASSWORD')))

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'prevstate':
                return ShowMenu(self.bot, self.chat_id, self.msg_to_del)

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        self.add_to_list()
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(back_button)
        return markup


class MoveToMyLists(BaseState):
    text = f"<b>Choose the list I should move to.</b>"
    sticker = "CAACAgIAAxkBAAEUcPRikTII9vknntnumjDxe9XdlDOAFgACIAADOPBYCPjmwRB3l-e8JAQ"

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data:
            if message.data == 'prevstate':
                return MyLists(self.bot, self.chat_id, self.msg_to_del)
            self.put_data(message.data)
            self.bot.send_message(self.chat_id, f"<b>The title was succesfully moved to {message.data} list</b>",
                                  parse_mode='html')
            ml = Lists(self.bot, self.chat_id, self.msg_to_del)
            ml.status = message.data
            return ml
        return MoveToMyLists(self.bot, self.chat_id, self.msg_to_del)

    def put_data(self, status):
        data = {
            "status": status
        }
        r = requests.put(f'http://127.0.0.1:8000/api/subscribers/{self.id}/', data=data,
                         auth=(os.getenv('USER'), os.getenv('PASSWORD')))

    def get_keyboard(self):
        markup = types.InlineKeyboardMarkup(row_width=1, )
        watching = types.InlineKeyboardButton('Watching 👀',
                                              callback_data='watching')
        completed = types.InlineKeyboardButton('Completed ✅',
                                               callback_data='completed')
        on_hold = types.InlineKeyboardButton('On Hold 🕓',
                                             callback_data='on_hold')
        dropped = types.InlineKeyboardButton('Dropped 🗑',
                                             callback_data='dropped')
        ptw = types.InlineKeyboardButton('Plan to watch 📝',
                                         callback_data='plan_to_watch')
        back_button = types.InlineKeyboardButton('Back ↩',
                                                 callback_data='prevstate')
        markup.add(watching, completed, on_hold, dropped, ptw, back_button)
        return markup
