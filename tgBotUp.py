# -*- coding: utf-8 -*-
import ctypes
import time
import datetime
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

DoneDay = []


class MyNotifi:
    def __init__(self):
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

        @self.bot.message_handler(commands=['start'])
        def start(message):
            global CHAT_ID
            xs = open('.envChat', 'w')
            xs.write(f"CHATID={str(message.chat.id)}")
            xs.close()
            CHAT_ID = os.getenv('CHATID')
            self.bot.send_message(message.chat.id, 'Бот успешно сохранил айди чата')
            load_dotenv('.envChat')
            load_dotenv('.envTok')
            self.CHAT_ID = os.getenv('CHATID')
            self.API_TOKEN = os.getenv('TOKEN')

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call: types.CallbackQuery):
            global DoneDay
            if call.message:
                if call.data not in DoneDay:
                    DoneDay.append(call.data)
                    # self.bot.send_message(self.CHAT_ID,f'{call.data} - Выполненно')
                    self.bot.edit_message_text(chat_id=self.CHAT_ID, message_id=call.message.id,
                                               text=f'{call.data} - Выполнено')
                else:
                    self.bot.delete_message(chat_id=self.CHAT_ID, message_id=call.message.id)

    def clearDone(self):
        global DoneDay
        DoneDay = []

    def gettime(self):
        logging.info('Отправил запрос на сайт')
        req = requests.get("https://aatime.ru/wp-content/themes/neve/eventspage-ajax.php", self.headers)
        src = req.text
        x = src.index('u0445:')
        ArchTime = src[x + 9:x + 14].split(':')
        return ArchTime

    def SendNotify(self, name, inf: str = 'Default'):
        global DoneDay
        time.sleep(0.5)
        CHAT_ID = os.getenv('CHATID')

        def zag():
            self.zagl = True

        try:
            with open("Archive/Tg_Bot/Save.txt", 'r') as file:
                fff = file.read().lstrip()
                save = json.loads(fff)
                if name in save and name not in DoneDay:
                    if name == 'Аукцион':
                        self.bot.send_message(CHAT_ID, f"\U0001F4B0 {inf[11:].replace('|,', '').replace(';', '')}")
                    elif name == 'Паки':
                        now = datetime.datetime.now()
                        now += datetime.timedelta(hours=8)
                        current_time = now.strftime("%H:%M")
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F4E9 Выручка от продажи паков будет выслана вам по почте в {current_time} по МСК')
                    elif name == 'Мирка':
                        self.bot.send_message(CHAT_ID, f'\U000026F5 Началась мирка на сверкашке, можно повозить :3')
                    elif name == 'Друг онлайн':
                        self.bot.send_message(CHAT_ID, f'\U0001F575 {inf[11:]}')
                    elif name == 'Вексели':
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        discord = types.InlineKeyboardButton("Дискорд", url='https://discord.gg/2Mqr9GTCGd')
                        markup.add(done, discord)

                        self.bot.send_message(CHAT_ID, f'\U0001F331 Не забудь сделать вексели\n'
                                                       f'узнать их ты можешь в дискорде по ссылке',
                                              reply_markup=markup)
                    elif name == 'Кирка':
                        self.bot.send_message(CHAT_ID, '\U000026CF У тебя откатилась новенькая кирка :D')
                    elif name == 'Новый день':
                        self.bot.send_message(CHAT_ID, '\U0001F313 Скоро рейд на новый день\n успей вступить!')
                    elif name == 'Даскшир':
                        self.bot.send_message(CHAT_ID, f'\U0001F6E1 Через 10 минут начнётся: {name}\n'
                                                       f' Только не стой афк)')
                    elif name == 'Спруты' or name == 'Око бури':
                        self.bot.send_message(CHAT_ID, f'\U0001F419 Через 10 минут начнётся: {name}, не пропусти!')
                    elif name == 'Кракен' or name == 'Левиафан':
                        self.bot.send_message(CHAT_ID, f'\U0001F419 Через 30 минут начнётся: {name}, не пропусти!')
                    elif name == 'Дельфиец':
                        self.bot.send_message(CHAT_ID, f'\U0001F30A Через 30 минут начнётся: {name}, не пропусти!')
                    elif name == 'Ксанатос':
                        self.bot.send_message(CHAT_ID, f'\U0001F432 Через 30 минут начнётся: {name}, не пропусти!')
                    elif name == 'Осада':
                        self.bot.send_message(CHAT_ID, f'\U0001F3AAЧерез 30 минут начнётся: {name}, не пропусти!')

                    elif name == 'Лицензии':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              "\U0001F4DC Не забудь выполнить лицензии!\n"
                                              "  Кладбище драконов - 5шт\n"
                                              "  Полуостров падающих звезд - 2шт\n"
                                              "  Золотые равнины - 2шт\n"
                                              "  Заболоченные низины - 3шт\n"
                                              "  Долгая коса - 2шт\n"
                                              "  Инистра - 1шт\n"
                                              "  Рокочущие перевалы - 2шт\n"
                                              "  Саванна - 5шт\n"
                                              "  Руины Харихараллы - 1шт\n"
                                              "  Хазира - 6шт", reply_markup=markup)
                    elif name == 'Порт-Аргенто':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F30A Не забудь сходить в {name}, бижутерия сама себя не сделает!',
                                              reply_markup=markup)

                    elif name == 'Библиотека':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U0001F4DA Не забудь сходить в {name}, булава сама себя не выбьет!',
                                              reply_markup=markup)
                    elif name == "Дейлики":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f"\U0001F55B Не забудь сделать дейлики!\n"
                                              "  Сокрытая долина: Зимний очаг\n"
                                              "  Сокрытая долина: Укромный утес\n"
                                              "  Колыбель мира: Сад матери\n"
                                              "  Ифнир: Каменные крылья", reply_markup=markup)
                    elif name == 'Мечи: Запад':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U00002694 Через 10 минут начнутся: {name}, не пропусти!\n'
                                              '  ППЗ: Рег.Община - кв у НПС, слева от входа в рег.общ.\n',
                                              reply_markup=markup)
                    elif name == 'Мечи: Восток':
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f'\U00002694 Через 10 минут начнутся: {name}, не пропусти!\n'
                                              '  Инистра: Рег.Община - кв у НПС, слева от входа в рег.общ.\n',
                                              reply_markup=markup)
                    elif name == "Эфен":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                        markup.add(done)
                        self.bot.send_message(CHAT_ID,
                                              f"\U00002694 Через 10 минут начнётся: {name}, не пропусти!\n"
                                              "  Эфен'Хал: Форпост Щ.И.Т.а - кв у НПС\n"
                                              "  Эфен'Хал: Форпост вашей фракции - Мобы",
                                              reply_markup=markup)
                    else:
                        if self.zagl:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            done = types.InlineKeyboardButton('|Выполнено:\U00002705|', callback_data=name)
                            markup.add(done)
                            if name == 'АГЛ(JMG)':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U00002694 Через 10 минут начнётся: {name}, не пропусти!\n'
                                                      '  Бездна: Нагашар - Ашъяра\n'
                                                      '  Солнечные поля - Глен, Лорея\n'
                                                      ' !Квест выдаётся при агре босса!',
                                                      reply_markup=markup)
                            elif name == 'Призрачка':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001F47B Через 10 минут начнётся: {name}, не пропусти!\n'
                                                      '  Запад:\n'
                                                      '     ППЗ: Рег.Община - Кв на табличке\n'
                                                      '     ППЗ: Застава - НПС для сдачи\n'
                                                      '  Восток:\n'
                                                      '     Инистра: Каор-Норд - Кв на табличке\n'
                                                      '     Инистра: Ривергард - НПС для сдачи',
                                                      reply_markup=markup)
                            elif name == 'Кровь':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001FA78 Через 10 минут начнётся: {name}, не пропусти!\n'
                                                      '  Запад:\n'
                                                      '     ППЗ: Рег.Община - Кв на выходе у НПС\n'
                                                      '  Восток:\n'
                                                      '     Инистра: Рег.Община - Кв на выходе у НПС',
                                                      reply_markup=markup)
                            elif name == 'Анталон':
                                self.bot.send_message(CHAT_ID,
                                                      f'\U0001F52E Через 10 минут начнётся: {name}, не пропусти!\n'
                                                      '  Солнечные поля - Кв дают при агре босса!\n'
                                                      '  p.s на месте тп можно взять квесты на кровь!',
                                                      reply_markup=markup)
                            else:
                                self.bot.send_message(CHAT_ID,
                                                      f'\U00002694 Через 10 минут начнётся: {name}, не пропусти!',
                                                      reply_markup=markup)
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
        schedule.every().day.at("00:00", timezone("Europe/Moscow")).do(self.clearDone)

        schedule.every().day.at("12:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Спруты')
        schedule.every().day.at("21:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Спруты')

        schedule.every().day.at("23:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Новый день')

        schedule.every().day.at("10:50", timezone("Europe/Moscow")).do(self.SendNotify, 'Даскшир')
        schedule.every().day.at("20:20", timezone("Europe/Moscow")).do(self.SendNotify, 'Дискшир')

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

        schedule.every(3).hours.do(self.SendNotify, 'Лицензии')
        schedule.every(5).hours.do(self.SendNotify, 'Вексели')
        schedule.every(4).hours.do(self.SendNotify, 'Дейлики')

        # schedule.every(3).seconds.do(self.SendNotify, 'Дейлики')
        # schedule.every(7).seconds.do(self.SendNotify, 'Лицензии')

        # schedule.every().day.at("03:00", timezone("Europe/Moscow")).do(self.SendNotify, 'Вексели')

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
                          encoding='utf-8') as mis:
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
                            self.SendNotify('Аук', i)
                            logs.remove(i)
                        if "Война в области «Сверкающее побережье» завершена." in i:
                            self.SendNotify('Мирка', i)
                            logs.remove(i)
                        if 'входит в игру.' in i:
                            self.SendNotify('Друг', i)
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
