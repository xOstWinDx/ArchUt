# -*- coding: utf-8 -*-
import ctypes
import logging
import getpass
import sys
import time
import locale
import psutil
import os
from datetime import datetime
import pystray
import PIL.Image

import guiLogic
import threading
import multiprocessing
import tgBotUp
from tendo import singleton
import ctypes

from ctypes.wintypes import MAX_PATH

dll = ctypes.windll.shell32
buf = ctypes.create_unicode_buffer(MAX_PATH + 1)

PATH_DOCU = f'C:\\Users\\{getpass.getuser()}\\Documents'
if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
    PATH_DOCU = buf.value
else:
    print("Failure!")



inRaid = False
gameON = False
ProgaOn = True
image = PIL.Image.open('Source/logo.ico')

ctypes.windll.shcore.SetProcessDpiAwareness(2)

locale.setlocale(locale.LC_TIME, ('ru_RU', 'UTF-8'))
locale.setlocale(locale.LC_CTYPE, ('ru_RU', 'UTF-8'))
logging.basicConfig(level=logging.INFO, filename="loggs\\ArchUt_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info('Начало лога')


def NotiftStart():
    try:
        notim = tgBotUp.MyNotifi()
        notim.StartBot()
    except Exception as X:
        logging.critical('Ошибка запуска потока бота', exc_info=True)


app: guiLogic.App = None
windowThread: threading.Thread = None


def window():
    global app
    try:

        app = guiLogic.App()
        print(app.winfo_screenwidth())
        # app.attributes("-topmost", True)
        app.iconbitmap(default="Source\\logo.ico")

        app.wm_protocol("WM_DELETE_WINDOW",
                        lambda: (app.withdraw(), app.rrrr()))
        # app.after(1000, app.ifclosed, ProgaOn)
        app.resizable(width=0, height=0)
        app.mainloop()
    except Exception as err:
        logging.critical('Ошибка запуска визуала', exc_info=True)


def on_clicked():
    global ProgaOn, windowThread, app

    if app.state() == 'normal':
        logging.info('Окно было свёрнуто')
        app.withdraw()
    else:
        app.deiconify()
        logging.info('Окно было развёрнуто')


def DetectedRaidIn():
    global PATH_DOCU
    try:
        os.remove(f"{PATH_DOCU}\\ArcheRage\\combat.log")
    except FileNotFoundError:
        logging.error('Нет файла для удаления', exc_info=True)


def inR():
    global inRaid
    if not inRaid:
        inRaid = True
        DetectedRaidIn()
        logging.info('Логи очистились')


def close(prog: pystray.Icon):
    global ProgaOn
    ProgaOn = False
    prog.stop()
    app.menuFrame.ProgaOn = False
    NotyProccess.terminate()
    app.doChatDump()
    app.quit()
    time.sleep(2)
    logging.info('Завершение.')
    sys.exit()


def outR():
    global inRaid
    inRaid = False
    if os.path.exists(f"{PATH_DOCU}\\ArcheRage\\combat.log"):
        if not os.path.exists('Archive'):
            os.mkdir('Archive')
        if not os.path.exists('Archive\\Combat'):
            os.mkdir('Archive\\Combat')
        logging.info("Закончилось отслеживание")
        now = datetime.now()
        logging.info(now)
        current_time = now.strftime("%d %b %Hч %Mм %Sс")
        name = '[' + str(current_time) + ']'
        os.mkdir(f'Archive\\Combat\\{name}')
        os.replace(f"{PATH_DOCU}\\ArcheRage\\combat.log",
                   f"Archive\\Combat\\{name}\\Комбо_{name}_Рейд.log")


    else:
        logging.info('ЛогиПустые')


def logListenner():
    global inRaid, gameON, ProgaOn
    ttt = open(f'{PATH_DOCU}\\ArcheRage\\Misc.log', 'w', encoding="utf-8")
    ttt.close()
    while ProgaOn:
        time.sleep(2)
        for process in psutil.process_iter():
            if process.name() == 'archeage.exe':
                gameON = True
                break
        if gameON and ProgaOn:

            time.sleep(2)
            try:
                with open(f"{PATH_DOCU}\\ArcheRage\\Misc.log", "r",
                          encoding='utf-8') as file:
                    logMisc = file.readlines()
                    for i in logMisc:
                        if 'присоединяется к отряду.' in i or 'присоединяется к рейду.' in i:
                            inR()
                            logMisc.remove(i)
                        if 'Вы покинули отряд' in i or 'расформирован.' in i or 'Вы покинули рейд.' in i and inRaid:
                            outR()
                            logMisc.remove(i)
                f = open(f"{PATH_DOCU}\\ArcheRage\\Misc.log", "w", encoding="utf-8")
                f.writelines(logMisc)
                f.close()
            except Exception as d:
                logging.error("Ошибка во время поиска выхода из отряда", exc_info=True)


if __name__ == '__main__':
    try:
        me = singleton.SingleInstance()
    except Exception:
        sys.exit()
    logging.info("Программа запустилась.")
    try:
        NotyProccess = multiprocessing.Process(target=NotiftStart, daemon=True)
        NotyProccess.start()
    except Exception:
        logging.error("Ошибка токена", exc_info=True)

    windowThread = threading.Thread(target=window, daemon=True)
    windowThread.start()
    icon = pystray.Icon('ArhUt', image, 'ArchUt', menu=pystray.Menu(
        pystray.MenuItem('Открыть', on_clicked, default=True),
        pystray.MenuItem('Очистить логи урона', inR),
        pystray.MenuItem("Взять логи как рейд", outR),
        pystray.MenuItem("Завершить", close)
    ))
    w = threading.Thread(target=logListenner, daemon=True)
    while app is None:
        time.sleep(0.1)
    w.start()
    on_clicked()
    icon.run()
