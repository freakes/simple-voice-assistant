from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pyttsx3
import speech_recognition as sr
from bs4 import BeautifulSoup
from translate import Translator
import time
from random import randint as rnd
from win10toast import ToastNotifier
import pyperclip
import requests as r
import webbrowser
import os

say_hello = True
__NAME__ = 'Мия'
__USER__ = 'Серёжа'
voice_engine = pyttsx3.init()

alphabet = ' 1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm'
dialogues_file = 'dialogues.txt'  # Файл с диалогами для логистической регрессии


class GenerateReplica:

    @staticmethod
    def clean_str(rr):
        rr = rr
        rr = [c for c in rr if c in alphabet]
        return ''.join(rr)

    with open('dialogues.txt', encoding='utf-8') as f:
        content = f.read()
    blocks = content.split('\n')
    dataset = []

    for block in blocks:
        replicas = block.split('\\')[:2]
        if len(replicas) == 2:
            pair = [GenerateReplica.clean_str(replicas[0]), GenerateReplica.clean_str(replicas[1])]
            if pair[0] and pair[1]:
                dataset.append(pair)
    print(dataset)

    X_text = []
    y = []
    for question, answer in dataset[:10000]:
        X_text.append(question)
        y += [answer]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)
    clf = LogisticRegression()
    clf.fit(X, y)

    @staticmethod
    def get_generative_replica(text):
        text_vector = vectorizer.transform([text]).toarray()[0]
        question = clf.predict([text_vector])[0]
        return question


class PasswordGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate():
        password = ''
        for i in range(10):
            password += chr(rnd(48, 123))
            password += '-' if i % 2 == 0 else ''

        pyperclip.copy(password)
        toaster = ToastNotifier()
        toaster.show_toast(f'Пароль скопирован в буфер обмена', icon_path='../lock.ico', msg='Мия', duration=3)
        pyperclip.copy(password)


class OpenPage:
    def __init__(self):
        self.vk = 'https://vk.com/feed'
        self.yt = 'https://www.youtube.com/'
        self.dstu = 'https://my.e.donstu.ru/gradebook_dstu/View'
        self.ymaps = 'https://yandex.ru/maps'
        self.gmail = 'https://mail.google.com/mail/u/0/#inboxs'

    @staticmethod
    def open(page):
        webbrowser.open(page)


class OpenApp:
    def __init__(self):
        self.telegram_path = r'C:\Users\ISerg\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Telegram Desktop\Telegram.lnk'
        self.discord_path = r'C:\Users\ISerg\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk'

    @staticmethod
    def open(path):
        os.startfile(path)


class Hello:
    def __init__(self):
        global __USER__
        self.__BYE_PHRASES__ = ['До скорого', 'До встречи', 'Пока',
                                'Спокойной ночи' if 20 <= int(
                                    time.strftime('%H', time.localtime())) <= 23 else 'Хорошего дня']
        self.__HELLO_PHRASES__ = [f'Привет {__USER__}', f'Привет, я {__NAME__}', Hello.hello(__USER__),
                                  'Привет, я скучала']

    def get_bye(self):
        return self.__BYE_PHRASES__

    def get_hi(self):
        return self.__HELLO_PHRASES__

    @staticmethod
    def hello(name):
        t = time.localtime()
        current_time = time.strftime("%H", t)
        if 7 <= int(current_time) < 12:
            return f'Доброе утро, {name}'
        elif 12 <= int(current_time) < 17:
            return f'Добрый день, {name}'
        elif 17 <= int(current_time):
            return f'Добрый вечер, {name}'
        else:
            return f'Доброй ночи, {name}'

# Парсинг с сайта синонимайзера
# class Synonym:
#     def __init__(self, word):
#         self.word = word
#         self.URL = f'https://text.ru/synonym/{word}'
#         self.page_4_parsing = r.get(self.URL)
#         self.class_4_parsing = 'ta-1'
#
#     def parse(self):
#         if self.page_4_parsing.status_code == 200:
#             soup = BeautifulSoup(self.page_4_parsing.text, 'html.parser')
#             all_synonyms = soup.find('body', class_='new-year')
#             all_synonyms = all_synonyms.find_all('div', class_='body__container')[2]
#             all_synonyms = all_synonyms.find('div', class_='synonym')
#             all_synonyms = all_synonyms.find('div', class_='fs-13')
#             all_synonyms = all_synonyms.find('div', {'id': 'data_container'})
#             all_synonyms = all_synonyms.find('div', {'id': 'list_synonyms'})
#             all_synonyms = all_synonyms.find('table', {'id': 'table_list_synonym'})
#             all_synonyms = all_synonyms.find_all('tr')
#             new_all_synonyms = []
#             new_all_synonyms_1 = []
#             new_all_synonyms_2 = []
#             i = 0
#             for el in all_synonyms[1::]:
#                 new_all_synonyms.append(el.find('td', class_='ta-l'))
#                 new_all_synonyms_1.append(new_all_synonyms[i].find('ALPHABET').text)
#                 new_all_synonyms_2.append(new_all_synonyms[i].find('ALPHABET').text.lower())
#                 i += 1
#             return new_all_synonyms_1 + new_all_synonyms_2
#         else:
#             return f'Ошибка {self.page_4_parsing.status_code}'


class Weather:
    def __init__(self):
        self.__API__ = '4341aeab39a5f417a23b111d6b9b70da'
        self.my_city = 'Rostov-on-Don,RU'

    def parse(self):
        try:
            res = r.get("http://api.openweathermap.org/data/2.5/weather",
                        params={'q': self.my_city, 'units': 'metric', 'lang': 'ru', 'APPID': self.__API__}
                        )
            data = res.json()
            return [f"На улице:", data['weather'][0]['description'],
                    f"Температура:", data['main']['temp'], '°',
                    f"Минимальная температура:", data['main']['temp_min'], '°',
                    f"Максимальная температура:", data['main']['temp_max'], '°']
        except Exception as ex:
            return "Exception (weather):", ex
            pass


class Translate:
    def __init__(self):
        global voice_engine
        self.translator = Translator(from_lang='ru', to_lang='en')

    @staticmethod
    def talk(_text):
        voice_engine.say(_text)
        voice_engine.runAndWait()

    def translate(self, _text):
        translated_text = self.translator.translate(_text)
        print(translated_text)
        self.talk(translated_text)

    def command(self):
        rec = sr.Recognizer()
        rec.dynamic_energy_threshold = False
        rec.energy_threshold = 1000
        rec.pause_threshold = 0.5

        with sr.Microphone() as source:
            print('Скажите что-то: ')
            rec.adjust_for_ambient_noise(source, duration=1)
            audio = rec.listen(source)
        try:
            recognized_text = rec.recognize_google(audio, language='ru-RU')
            return recognized_text

        except sr.UnknownValueError:
            self.talk('Повторите ещё раз')
            recognized_text = command()

        return recognized_text


class Talking:
    def __init__(self):
        self.was_hello = False

    def set_was_hello(self, val):
        self.was_hello = val

    @staticmethod
    def command():
        global say_hello, T
        h = Hello()
        rec = sr.Recognizer()

        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source, duration=1)
            audio = rec.listen(source)
        try:
            print(213231)
            recognized_text = rec.recognize_google(audio, language='ru-RU')
            if recognized_text == 'Привет Мия' or recognized_text == 'привет мия' \
                    or recognized_text == 'Привет мия' or recognized_text == 'привет Мия':
                T.set_was_hello(True)
                if say_hello:
                    Communication.talk(h.get_hi()[rnd(0, 3)])
                say_hello = False
            return recognized_text

        except sr.UnknownValueError:
            if T.was_hello:
                Communication.talk('Повторите ещё раз')
            recognized_text = Talking.command()

        return recognized_text


T = Talking()


def handle_command(command):
    global T
    new_command = command
    command = ''
    for c in new_command:
        c = c.lower()
        command += c + ' '
    reply = GenerateReplica.get_generative_replica(command)
    if T.was_hello:
        Communication.talk(reply)
    return reply


class Communication:
    def __init__(self):
        global voice_engine, T
        self._text = Talking.command()

    @staticmethod
    def talk(_text):
        print(_text)
        voice_engine.say(_text)
        voice_engine.runAndWait()

    def simple_communication(self):
        oa = OpenApp()
        op = OpenPage()
        _text_l = self._text.split(' ')
        get_reply = handle_command(_text_l)
        # Погода
        if get_reply == 'сверяю термометры':
            Communication.talk(Weather().parse())
        # Переводчик
        if get_reply == 'слушаю':
            tr = Translate()
            tr.translate(tr.command())
        # Прощание
        if get_reply == 'уже скучаю':
            T.set_was_hello(False)

        if get_reply == 'открываю discord':
            oa.open(oa.discord_path)

        if get_reply == 'открываю telegram':
            oa.open(oa.telegram_path)

        if get_reply == 'открываю журнал':
            op.open(op.dstu)

        if get_reply == 'открываю вконтакте':
            op.open(op.vk)

        if get_reply == 'генерирую пароль':
            PasswordGenerator.generate()

        if get_reply == 'открываю ящик':
            op.open(op.gmail)

        if get_reply == 'открываю youtube':
            op.open(op.yt)

        if get_reply == 'открываю яндекс карты':
            op.open(op.ymaps)


while True:
    communicator = Communication()
    communicator.simple_communication()
