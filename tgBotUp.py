# -*- coding: utf-8 -*-
import ctypes
import time
import datetime
from datetime import date
import json
import requests
from dotenv import load_dotenv
from pytz import timezone
import schedule
import telebot
from telebot import types
import os
import getpass
import threading
import logging
from ctypes.wintypes import MAX_PATH

dll = ctypes.windll.shell32
buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
PATH_DOCU = fr'C:\Users\{getpass.getuser()}\Documents'
if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
    PATH_DOCU = buf.value
else:
    logging.error("Не удалось получить доки (тгбот)")

logging.basicConfig(level=logging.INFO, filename="loggs\\ArchUt.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

DoneDayDefault = {'DATEDAY': date.today().day, 'АГЛ(JMG)': True, 'Кровь': True, 'Призрачка': True, 'Анталон': True,
                  'Лицензии': True, 'Вексели': True, 'Порт-Аргенто': True, 'Библиотека': True,
                  'Дейлики': True, 'Эфен': True, 'Бухта': True, 'Даскшир': True, 'Гартрейн': True, 'Мечи: Запад': True,
                  'Мечи: Восток': True, 'Спруты': True, "Рубеж": True, }
DoneDay = DoneDayDefault


class MyNotifi:
    def __init__(self):
        global DoneDay
        self.zagl = True
        self.tm = None
        self.st_accept = "text/html"  # говорим веб-серверу,
        # что хотим получить html
        # имитируем подключение через браузер Mozilla на macOS
        st_useragent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 "
            "Safari/605.1.15")
        # формируем хеш заголовков
        self.headers = {
            "Accept": self.st_accept,
            "User-Agent": st_useragent
        }

        # считываем текст HTML-документа
        while True:
            time.sleep(5)
            logging.info('Пытаюсь получить токен')
            if not os.path.exists('.envChat'):
                logging.error('Нет файла с чат айди')
                x = open('.envChat', 'w', encoding='utf-8')
                x.write('')
                x.close()
            if not os.path.exists('.envTok'):
                logging.error('Нет файла с токеном')
                x = open('.envTok', 'w', encoding='utf-8')
                x.write('')
                x.close()
            load_dotenv('.envChat')
            load_dotenv('.envTok')
            self.CHAT_ID = os.getenv('CHATID')
            self.API_TOKEN = os.getenv('TOKEN')
            try:
                if len(self.API_TOKEN) > 5:
                    self.bot = telebot.TeleBot(self.API_TOKEN)
                    t1 = threading.Thread(target=self.bot.polling)
                    t1.start()
                break
            except Exception:
                logging.warning('Токен не верный')
        logging.info("Успешно соеденился с ботом")

        if os.path.exists('Archive/DumpDay.txt'):
            with open('Archive/DumpDay.txt', 'r', encoding='utf-8') as day:
                dayd = day.read()
                DoneDay = json.loads(dayd)
                print(DoneDay)
        else:
            with open('Archive/DumpDay.txt', 'w', encoding='utf-8') as dayz:
                json.dump(DoneDay, dayz)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            global CHAT_ID
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            but1 = types.KeyboardButton('Что сегодня осталось сделать?')
            but2 = types.KeyboardButton('Помощь по использованию бота', )
            markup.add(but1)
            markup.add(but2)
            xs = open('.envChat', 'w')
            xs.write(f"CHATID={str(message.chat.id)}")
            xs.close()
            CHAT_ID = os.getenv('CHATID')
            self.bot.send_message(message.chat.id, 'Бот успешно сохранил айди чата', reply_markup=markup)
            load_dotenv('.envChat')
            load_dotenv('.envTok')
            self.CHAT_ID = os.getenv('CHATID')
            self.API_TOKEN = os.getenv('TOKEN')

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call: types.CallbackQuery):
            global DoneDay, DoneDayDefault
            if call.message:
                if DoneDay[call.data]:
                    DoneDay[call.data] = False
                    # self.bot.send_message(self.CHAT_ID,f'{call.data} - Выполненно')
                    self.bot.edit_message_text(chat_id=self.CHAT_ID, message_id=call.message.id,
                                               text=f'{call.data} - Выполнено')
                    logging.info(f"Пометил как выполненное: {call.data}")
                else:
                    self.bot.delete_message(chat_id=self.CHAT_ID, message_id=call.message.id)
                    logging.info(f"Уже нажимал, чо?: {call.data}")
                with open('Archive/DumpDay.txt', 'w', encoding='utf-8') as dayz:
                    json.dump(DoneDay, dayz)

        @self.bot.message_handler(content_types=['text'])
        def status(message: types.Message):
            global DoneDay
            gartCheck = False
            if message.text == 'Что сегодня осталось сделать?':
                with open("Archive/Tg_Bot/Save.txt", 'r') as file:
                    fff = file.read().lstrip()
                    save: list = json.loads(fff)
                    for i in ['Око бури', 'Осада', 'Ксанатос', 'Дельфиец', 'Гартрейн', 'Кракен', 'Левиафан',
                              'Мирка-Cевер', 'Кирка', 'Друг онлайн', 'Аукцион', 'Паки', 'Новый день']:
                        if i in save:
                            if i == 'Гартрейн':
                                gartCheck = True
                            save.remove(i)
                    DDmax = len(save)
                    if date.today().isoweekday() in (7, 1, 3, 5):
                        DDmax += 1
                        save.append("Гартрейн")
                    print(save)
                    print(DDmax)
                    if len(save) == 0:
                        self.bot.send_message(self.CHAT_ID, '<b>У вас нет отслеживаемых ивентов!</b>',
                                              parse_mode='HTML')
                        return 0
                for i in ['Лицензии', 'Вексели', 'Порт-Аргенто', 'Библиотека', 'Рубеж', "Дейлики"]:
                    if DoneDay[i]:
                        self.SendNotify(i)
                        if i in save:
                            DDmax -= DoneDay[i]
                for i in ['АГЛ(JMG)', 'Кровь', 'Призрачка', 'Анталон', 'Эфен', 'Бухта', 'Даскшир', 'Мечи: Запад',
                          'Мечи: Восток',
                          'Спруты']:

                    if i in save and DoneDay.get(i, True):
                        DDmax -= DoneDay[i]
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|',
                                                          callback_data=i)
                        markup.add(done)
                        self.bot.send_message(self.CHAT_ID, f"<b>Сегодня</b> нужно ещё сделать: <b>{i}</b>",
                                              reply_markup=markup, parse_mode='HTML')
                print(DoneDay)
                if date.today().isoweekday() in (7, 1, 3, 5) and gartCheck and DoneDay.get('Гартрейн', True):
                    DDmax -= DoneDay.get('Гартрейн', True)
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    done = types.InlineKeyboardButton('|Выполнено:\U00002705|',
                                                      callback_data='Гартрейн')
                    markup.add(done)
                    self.bot.send_message(self.CHAT_ID, f"<b>Сегодня</b> нужно ещё сделать: <b>Гартрейн</b>",
                                          reply_markup=markup, parse_mode='HTML')
                if DDmax == len(save):
                    self.bot.send_message(self.CHAT_ID, f"<b>ВСЁ СДЕЛАНО!</b>",
                                          parse_mode='HTML')
            if message.text == 'Помощь по использованию бота':
                self.bot.send_message(self.CHAT_ID,
                                      '<a href="https://alekseis-organization-2.gitbook.io/untitled/#about">Документация</a>',
                                      parse_mode="HTML")

    def gettime(self):
        logging.info('Отправил запрос на сайт')
        req = requests.get("https://aatime.ru/wp-content/themes/neve/eventspage-ajax.php", self.headers)
        src = req.text
        x = src.index('u0445:')
        ArchTime = src[x + 9:x + 14].split(':')
        return ArchTime

    def SendNotify(self, name, inf: str = 'Default'):
        global DoneDay, DoneDayDefault
        logging.info(f"Прилетел увед: {name}")
        CHAT_ID = os.getenv('CHATID')

        def zag():
            self.zagl = True

        try:
            with open("Archive/Tg_Bot/Save.txt", 'r') as file:
                fff = file.read().lstrip()
                save = json.loads(fff)
                if DoneDay['DATEDAY'] != date.today().day:
                    DoneDay = DoneDayDefault
                    print("ПОСТАВИЛ ДЕФОЛТ!")
                    with open('Archive/DumpDay.txt', 'w', encoding='utf-8') as dayz:
                        json.dump(DoneDay, dayz)
                if name == 'Рестарт':
                    self.bot.send_message(CHAT_ID, f'<b>ЧЕРЕЗ 30 МИНУТ РЕСТАРТ СЕРВА!</b>',
                                          parse_mode='HTML')
                if name in save and DoneDay.get(name, True):

                    print("Прилетел увед и его значение: ", DoneDay.get(name, True))
                    logging.info(f"увед успешно отправлен: {name}")
                    if name == 'Аукцион':
                        self.bot.send_message(CHAT_ID, f"\U0001F4B0 {inf[11:].replace('|,', '').replace(';', '')}")
                    elif name == 'Паки':
                        now = datetime.datetime.now()
                        now += datetime.timedelta(hours=8)
                        current_time = now.strftime("%H:%M")
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F4E9 <b>Выручка</b> от продажи паков будет выслана вам по почте '
                                              f'в <b>{current_time}</b> по МСК',
                                              parse_mode='HTML')
                    elif name == 'Мирка-Cевер':
                        self.bot.send_message(CHAT_ID, f'\U000026F5 Началась мирка на <b>сверкашке</b>, можно повозить',
                                              parse_mode='HTML')
                    elif name == 'Друг онлайн':
                        self.bot.send_message(CHAT_ID, f'\U0001F575 {inf[11:]}')
                    elif name == 'Вексели':
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|',
                                                          callback_data=name)
                        discord = types.InlineKeyboardButton("Дискорд", url='https://discord.gg/2Mqr9GTCGd')
                        markup.add(done, discord)

                        self.bot.send_message(CHAT_ID, f'\U0001F331 <b>Не забудь</b> сделать <b>векселя</b>\n'
                                                       f'узнать их ты можешь в дискорде по ссылке', parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == 'Кирка':
                        self.bot.send_message(CHAT_ID, '\U000026CF У тебя откатилась <b>новенькая кирка</b>',
                                              parse_mode='HTML')
                    elif name == 'Новый день':
                        self.bot.send_message(CHAT_ID, '\U0001F313 Скоро рейд на <b>новый день</b>\n успей вступить!',
                                              parse_mode='HTML')
                    elif name == 'Даскшир':
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|',
                                                          callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID, f'\U0001F6E1 Через <b>10 минут</b> начнётся: <b>{name}</b>\n',
                                              parse_mode='HTML', reply_markup=markup)
                    elif name == 'Спруты' or name == 'Око бури':
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|',
                                                          callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F419 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              parse_mode='HTML', reply_markup=markup)
                    elif name == 'Кракен' or name == 'Левиафан':
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F419 Через <b>30 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              parse_mode='HTML')
                    elif name == 'Дельфиец':
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F30A Через <b>30 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              parse_mode='HTML')
                    elif name == 'Ксанатос':
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F432 Через <b>30 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              parse_mode='HTML')
                    elif name == 'Осада':
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F3AAЧерез <b>30 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              parse_mode='HTML')

                    elif name == 'Лицензии':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              "\U0001F4DC <b>Не забудь</b> выполнить <b>лицензии!</b>\n"
                                              "  Кладбище драконов - <b>5шт</b>\n"
                                              "  Полуостров падающих звезд - <b>2шт</b>\n"
                                              "  Золотые равнины - <b>2шт</b>\n"
                                              "  Заболоченные низины - <b>3шт</b>\n"
                                              "  Долгая коса - <b>2шт</b>\n"
                                              "  Инистра - <b>1шт</b>\n"
                                              "  Рокочущие перевалы - <b>2шт</b>\n"
                                              "  Саванна - <b>5шт</b>\n"
                                              "  Руины Харихараллы - <b>1шт</b>\n"
                                              "  Хазира - <b>6шт</b>",
                                              parse_mode='HTML', reply_markup=markup)
                    elif name == 'Порт-Аргенто':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F30A <b>Не забудь</b> сходить в <b>{name}</b>',
                                              parse_mode="HTML",
                                              reply_markup=markup)

                    elif name == 'Библиотека':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F4DA <b>Не забудь</b> сходить в <b>Библиотеку</b>',
                                              parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == 'Рубеж':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F311 <b>Не забудь</b> сделать <b>Последний Рубеж</b>',
                                              parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == "Дейлики":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f"\U0001F55B <b>Не забудь</b> сделать <b>дейлики!</b>\n"
                                              "  Сокрытая долина: Зимний <b>Очаг</b>\n"
                                              "  Сокрытая долина: Укромный <b>Утес</b>\n"
                                              "  Колыбель мира: <b>Сад</b> матери\n"
                                              "  Ифнир: Каменные <b>Крылья</b>", parse_mode='HTML', reply_markup=markup)
                    elif name == 'Мечи: Запад':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U00002694 Через <b>10 минут</b> начнутся: <b>{name}</b>, не пропусти!\n'
                                              '  <u>ППЗ: Рег.Община</u> - кв у НПС, слева от входа в рег.общ.\n',
                                              parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == 'Мечи: Восток':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U00002694 Через <b>10 минут</b> начнутся: <b>{name}</b>, не пропусти!\n'
                                              '  <u>Инистра: Рег.Община</u> - кв у НПС, слева от входа в рег.общ.\n',
                                              parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == "Эфен":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f"\U00002694 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n"
                                              "  <u>Эфен'Хал: Форпост Щ.И.Т.а</u> - кв у НПС\n"
                                              "  <u>Эфен'Хал: Форпост вашей фракции</u> - Мобы", parse_mode='HTML',
                                              reply_markup=markup)
                    elif name == "Бухта":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f"\U00002694 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n"
                                              "  <u>Бухта китобоев: Форпост Щ.И.Т.а</u> - кв у НПС\n"
                                              "  <u>Бухта китобоев: Форпост вашей фракции</u> - Мобы",
                                              parse_mode='HTML',
                                              reply_markup=markup)

                    elif name == 'Гартрейн':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U00002694 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                              reply_markup=markup, parse_mode='HTML')

                    else:
                        if self.zagl:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                            markup.add(done)
                            if name == 'АГЛ(JMG)':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U00002694 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n'
                                                      '  <u>Бездна: Нагашар</u> - Ашъяра\n'
                                                      '  <u>Солнечные поля</u> - Глен, Лорея\n'
                                                      ' <b>!Квест выдаётся при агре босса!</b>', parse_mode='HTML',
                                                      reply_markup=markup)
                            elif name == 'Призрачка':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001F47B Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n'
                                                      '  <b>Запад:</b>\n'
                                                      '     <u>ППЗ: Рег.Община</u> - Кв на табличке\n'
                                                      '     <u>ППЗ: Застава</u> - НПС для сдачи\n'
                                                      '  <b>Восток:</b>\n'
                                                      '     <u>Инистра: Каор-Норд</u> - Кв на табличке\n'
                                                      '     <u>Инистра: Ривергард</u> - НПС для сдачи',
                                                      parse_mode='HTML',
                                                      reply_markup=markup)
                            elif name == 'Кровь':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001FA78 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n'
                                                      '  <b>Запад:</b>\n'
                                                      '     <u>ППЗ: Рег.Община</u> - Кв на выходе у НПС\n'
                                                      '  <b>Восток:</b>\n'
                                                      '     <u>Инистра: Рег.Община</u> - Кв на выходе у НПС',
                                                      parse_mode='HTML',
                                                      reply_markup=markup)
                            elif name == 'Анталон':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001F52E Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!\n'
                                                      '  <u>Солнечные поля</u> - Кв дают при агре босса!\n'
                                                      '  <b>p.s на месте тп можно взять квесты на кровь!</b>',
                                                      parse_mode='HTML',
                                                      reply_markup=markup)

                            else:
                                self.bot.send_message(CHAT_ID,
                                                      f'\U00002694 Через <b>10 минут</b> начнётся: <b>{name}</b>, не пропусти!',
                                                      reply_markup=markup, parse_mode='HTML')
                            self.zagl = False
                            threading.Timer(500, zag).start()
                            logging.info(f'Поставил заглушку {self.zagl}')
        except Exception:
            logging.error("Увед багнулся", exc_info=True)

    def DoNotifyInGameTime(self):
        def updatetime():
            while True:
                time.sleep(200)
                times = self.gettime()
                self.tm = datetime.timedelta(hours=int(times[0]), minutes=int(times[1]))
                logging.info(f'Скорректировал время {self.tm}')

        times = self.gettime()
        self.tm = datetime.timedelta(hours=int(times[0]), minutes=int(times[1]))
        threading.Thread(target=updatetime, daemon=True).start()
        while True:
            self.tm += datetime.timedelta(0, 6)
            if datetime.timedelta(hours=4, minutes=50) < self.tm < datetime.timedelta(hours=5, minutes=10):
                self.SendNotify("АГЛ(JMG)")
                logging.info(f'АГЛ(JMG) {self.tm} {self.zagl}')

            if datetime.timedelta(hours=10, minutes=50) < self.tm < datetime.timedelta(hours=11, minutes=10):
                self.SendNotify("Кровь")
                logging.info(f'Кровь {self.tm} {self.zagl}')

            if datetime.timedelta(hours=22, minutes=50) < self.tm < datetime.timedelta(hours=23, minutes=10):
                self.SendNotify("Призрачка")
                logging.info(f'Призрачка {self.tm} {self.zagl}')

            if datetime.timedelta(hours=16, minutes=50) < self.tm < datetime.timedelta(hours=17, minutes=10):
                self.SendNotify("Анталон")
                logging.info(f'Анталон {self.tm} {self.zagl}')
            time.sleep(1)

    def DoNotifyRealTime(self):

        schedule.every().day.at("12:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Спруты')
        schedule.every().day.at("21:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Спруты')

        schedule.every().day.at("23:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Новый день')
        schedule.every().wednesday.at("00:30", timezone("Europe/Moscow")).do(self.SendNotify, 'Рестарт')

        schedule.every().day.at("20:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Даскшир')
        schedule.every().day.at("10:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Даскшир')

        schedule.every().sunday.at("10:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().sunday.at("19:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().monday.at("10:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().monday.at("19:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().wednesday.at("10:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().wednesday.at("19:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().friday.at("10:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')
        schedule.every().friday.at("19:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Гартрейн')

        schedule.every().day.at('19:45', timezone("Europe/Moscow")).do(self.SendNotify, 'Дельфиец')

        schedule.every().tuesday.at('19:35', timezone("Europe/Moscow")).do(self.SendNotify, 'Левиафан')
        schedule.every().thursday.at('19:35', timezone("Europe/Moscow")).do(self.SendNotify, 'Левиафан')
        schedule.every().saturday.at('19:35', timezone("Europe/Moscow")).do(self.SendNotify, 'Левиафан')

        schedule.every().wednesday.at('20:30', timezone("Europe/Moscow")).do(self.SendNotify, 'Осада')

        schedule.every().tuesday.at('21:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Ксанатос')
        schedule.every().thursday.at('21:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Ксанатос')
        schedule.every().sunday.at('21:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Ксанатос')

        schedule.every().tuesday.at('22:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Кракен')
        schedule.every().thursday.at('22:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Кракен')
        schedule.every().sunday.at('22:00', timezone("Europe/Moscow")).do(self.SendNotify, 'Кракен')

        schedule.every().tuesday.at("20:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Око бури')
        schedule.every().thursday.at("20:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Око бури')
        schedule.every().saturday.at("20:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Око бури')

        schedule.every(1).hours.do(self.SendNotify, 'Лицензии')
        schedule.every().day.at("23:10", timezone("Europe/Moscow")).do(self.SendNotify, 'Лицензии')
        schedule.every(50).minutes.do(self.SendNotify, 'Вексели')
        schedule.every().day.at("23:45", timezone("Europe/Moscow")).do(self.SendNotify, 'Вексели')
        schedule.every(70).minutes.do(self.SendNotify, 'Дейлики')
        schedule.every().day.at("23:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Дейлики')
        schedule.every(2).hours.do(self.SendNotify, 'Библиотека')
        schedule.every().day.at("22:40", timezone("Europe/Moscow")).do(self.SendNotify, 'Библиотека')
        schedule.every(90).minutes.do(self.SendNotify, 'Порт-Аргенто')
        schedule.every().day.at("22:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Порт-Аргенто')
        schedule.every(100).minutes.do(self.SendNotify, 'Рубеж')
        schedule.every().day.at("23:30", timezone("Europe/Moscow")).do(self.SendNotify, 'Рубеж')

        # schedule.every(2).seconds.do(self.SendNotify, 'Спруты')
        # schedule.every(2).seconds.do(self.SendNotify, 'Даскшир')
        # schedule.every(2).seconds.do(self.SendNotify, 'Гартрейн')

        while True:
            schedule.run_pending()
            time.sleep(1)

    def doKirkaTimer(self):
        self.SendNotify('Кирка')

    def DoLogsNotify(self):
        global PATH_DOCU
        pakTh = threading.Timer(120, self.SendNotify, ['Паки', 'Gg'])
        while True:
            try:
                with open(fr"{PATH_DOCU}\ArcheRage\Misc.log", "r",
                          encoding='utf-8', errors='replace') as mis:
                    logs = mis.readlines()
                    for i in logs:
                        if "области «Полуостров Падающих Звезд» назрел конфликт." in i:
                            self.SendNotify('Мечи: Запад')
                            logs.remove(i)
                        if 'области «Инистра» назрел конфликт' in i:
                            self.SendNotify('Мечи: Восток')
                            logs.remove(i)
                        if "области «Эфен'Хал» назрел конфликт." in i:
                            self.SendNotify('Эфен')
                            logs.remove(i)
                        if "области «Бухта китобоев» началась война." in i:
                            self.SendNotify('Бухта')
                            logs.remove(i)
                        if "Выручка от сделки будет выслана вам по почте в течение 8 часов." in i:
                            if pakTh.is_alive():
                                pakTh.cancel()
                                pakTh = threading.Timer(120, self.SendNotify, ['Паки', i])
                                pakTh.start()
                            else:
                                pakTh = threading.Timer(120, self.SendNotify, ['Паки', i])
                                pakTh.start()
                            logs.remove(i)
                        if "выкуплен с аукциона" in i:
                            self.SendNotify('Аукцион', i)
                            logs.remove(i)
                        if "Война в области «Сверкающее побережье» завершена." in i:
                            self.SendNotify('Мирка-Cевер', i)
                            logs.remove(i)
                        if 'входит в игру.' in i:
                            self.SendNotify('Друг онлайн', i)
                            logs.remove(i)
                        if 'Использовано: [Новенькая кирка]' in i:
                            s = 'Кирка'
                            logging.info("Кирку нашёл")
                            threading.Timer(10800, self.SendNotify, args=[s]).start()
                            logs.remove(i)
                f = open(fr"{PATH_DOCU}\ArcheRage\Misc.log", "w", encoding="utf-8")
                f.writelines(logs)
                f.close()
                time.sleep(2)
            except Exception:
                logging.error("Ошибка бота, чтения логов", exc_info=True)
                time.sleep(2)
                continue

    def StartBot(self):
        try:

            n1 = threading.Thread(target=self.DoNotifyRealTime, daemon=True)
            n1.start()

            n2 = threading.Thread(target=self.DoNotifyInGameTime, daemon=True)
            n2.start()
            n3 = threading.Thread(target=self.DoLogsNotify, daemon=True)
            n3.start()
            logging.info("Запустил все потоки бота")
        except Exception as x1:
            logging.critical("Ошибка запуска потоков бота", exc_info=True)
            exit(0)
