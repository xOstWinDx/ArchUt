# -*- coding: utf-8 -*-
import datetime
import getpass
import os
import sys
import time

import telebot
import telebot.apihelper
import json
import _tkinter
import customtkinter
from PIL import Image
import logicMain
import threading
from googletrans import Translator
import logging

customtkinter.set_appearance_mode("dark")

Id_Dir = {}
logging.basicConfig(level=logging.INFO, filename="loggs\\ArchUt.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class getSpisok():
    global Id_Dir

    @staticmethod
    def OldgetSpisok():
        asp = os.listdir('Archive/Combat')
        for i in asp:
            logicMain.AnalyseLogAndDoGraph.DoHealAndDamage(i.rstrip())
        return asp if len(asp) > 0 else ['Нет записей']

    @staticmethod
    def getSpisok():
        global Id_Dir
        try:
            with open('Archive\\IdDir.txt', 'r', encoding='utf-8') as idfd:
                xx = idfd.read().strip()
                Id_Dir = json.loads(xx)
        except:
            pass
        if not os.path.exists('Archive'):
            os.mkdir('Archive')
        if not os.path.exists('Archive\\Combat'):
            os.mkdir('Archive\\Combat')
        with open('Archive\\IdDir.txt', 'w', encoding='utf-8') as idfd:
            xx = os.listdir('Archive/Combat')
            for i in xx:
                if i.strip() not in Id_Dir and i.strip() != '':
                    Id_Dir[i.strip()] = i.strip()
            json.dump(Id_Dir, idfd)
        for i in Id_Dir.keys():
            print(i)
            logicMain.AnalyseLogAndDoGraph.DoHealAndDamage(Id_Dir[i])
        idfd.close()
        return [Id_Dir.keys(), Id_Dir.values()] if len(Id_Dir) > 0 else [['Нет записей'], ['Нет записей']]


class MyCheckFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values
        self.checkboxes = []
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title = customtkinter.CTkLabel(self, text='Funk', fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkSwitch(self, text=value, font=("TkDefaultFont", 16), command=self.tuk,
                                               switch_width=45, switch_height=22)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="wesn")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    def tuk(self):
        if not os.path.exists('Archive\\Tg_Bot'):
            os.mkdir('Archive\\Tg_Bot')
        fff = open('Archive\\Tg_Bot\\Save.txt', 'w')
        x = self.get()
        json.dump(x, fff)

    def sett(self):
        try:
            with open("Archive/Tg_Bot/Save.txt", 'r') as file:
                fff = file.read().lstrip()
                save = json.loads(fff)
                for ch in self.checkboxes:
                    if ch.cget('text') in save:
                        ch.select()
                    else:
                        ch.deselect()
        except FileNotFoundError:
            logging.error("Нет сейва бота", exc_info=True)
        except json.decoder.JSONDecodeError:
            logging.error("файл бота ошибка", exc_info=True)


class MyTgBotFtame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)
        self.leftFr = customtkinter.CTkFrame(self)
        self.leftFr.rowconfigure(0, weight=1)
        self.leftFr.columnconfigure(1, weight=1)
        self.rightFg = customtkinter.CTkFrame(self)
        self.checkbox = MyCheckFrame(self.leftFr,
                                     values=['АГЛ', 'Кровь', 'Призрачка', 'Анталон', 'Гроза над морем',
                                             'Новый день', 'Вексели', 'Даскшир', 'Гартрейн', 'Око бури', 'Мечи', 'Эфен',
                                             'Бухта',
                                             'Паки', 'Аук',
                                             'Мирка', 'Друг', 'Кирка', 'Осада', 'Ксанатос', 'Дельфиец', 'Кракен',
                                             'Левиафан'])

        self.checkbox.grid(row=0, column=0, sticky='nsew')
        self.checkbox.grid(row=0, column=0, sticky='nsew')
        self.leftFr.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        self.my_image = customtkinter.CTkImage(light_image=Image.open("Source/back.jpg"), size=(780, 558))

        image_label = customtkinter.CTkLabel(self.rightFg, image=self.my_image, text='')
        self.rightFg.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)
        self.rigBar = customtkinter.CTkFrame(self.rightFg)
        self.rigBar.columnconfigure((0), weight=1)
        self.entry = customtkinter.CTkEntry(self.rigBar, font=("TkDefaultFont", 16, 'bold'))
        self.entry.bind("<Button-1>", self.handl_click)
        self.entry.bind('<Return>', process)
        self.entry.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

        self.butapply = customtkinter.CTkButton(self.rigBar, text='Apply', command=self.savaTok)
        self.butapply.grid(row=0, column=1, columnspan=1, sticky='nsew', padx=4, pady=4)

        self.rigBar.grid(row=1, column=1, sticky='nsew', padx=4, pady=4)

        image_label.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)

    def handl_click(self, event):
        if self.entry.cget('text_color') == 'LightCoral' and len(self.entry.get()) > 0:
            self.entry.delete(0, last_index=customtkinter.END)
            self.entry.configure(text_color='white')

    def savaTok(self):
        if self.entry.cget('state') != 'disabled':
            try:
                if self.entry.get() != '':
                    bot = telebot.TeleBot(token=self.entry.get())
                    try:
                        bot_info = bot.get_me()
                    except telebot.apihelper.ApiTelegramException:
                        logging.warning("Ошибка токена, проверьте его на правильность")
                        self.entry.delete(0, last_index=customtkinter.END)
                        self.entry.configure(text_color='LightCoral')
                        self.entry.insert(0, 'Ошибка токена, проверьте его на правильность!')
                    else:
                        logging.info("Бот авторизован")
                        with open('.envTok', 'w', encoding="utf-8") as file:
                            file.write(f"TOKEN={self.entry.get()}")
                        self.entry.delete(0, last_index=customtkinter.END)
                        self.entry.configure(text_color='LightGreen')

                        self.entry.insert(0, 'Бот авторизован!')
                        self.entry.configure(state='disabled')

            except FileNotFoundError:
                logging.error("Ошибка с файлами во время сохранения токена", exc_info=True)


class MyMenuFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.now = None
        self.grid_columnconfigure((3, 4), weight=3)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.MyDamage = MyMainWindowFrame(self.master, title='Damage',
                                          comandUpd=self.updateFrame)
        self.MyHeal = MyMainWindowFrame(self.master, title='Heal', comandUpd=self.updateFrame)

        self.MyTank = MyMainWindowFrame(self.master, title='Tank', comandUpd=self.updateFrame)

        self.text_bar = ''
        self.MyTrans = customtkinter.CTkFrame(self.master, height=600)
        self.radio = MyRadiobuttonFrame(self.MyTrans,
                                        printBut=self.pressChanRadio,
                                        title="Chats")
        self.textbox = customtkinter.CTkTextbox(self.MyTrans, height=600, width=800, font=("TkDefaultFont", 13))
        self.textbox.insert("0.0", self.text_bar)

        self.delBut = customtkinter.CTkButton(self.MyTrans, text="Удалить", command=self.delbutton)
        self.MyTrans.rowconfigure(0, weight=1)
        self.textbox.grid(row=0, column=1, sticky="nsew", pady=3, padx=3, columnspan=4, rowspan=2)
        self.radio.grid(row=0, column=0, sticky='nsew', rowspan=1, padx=3, pady=3)
        self.delBut.grid(row=1, column=0, sticky='we', rowspan=1, padx=3, pady=3)

        self.MyTgBot = MyTgBotFtame(self.master)
        self.ProgaOn = True

        self.activWind = None

        self.MyBack = customtkinter.CTkFrame(self)
        self.my_image = customtkinter.CTkImage(light_image=Image.open("Source/image.png"), size=(990, 600), )
        image_label = customtkinter.CTkLabel(self.MyBack, image=self.my_image, text='')
        self.MyBack.grid(row=1, column=0, columnspan=5, pady=3, padx=3)
        image_label.grid(row=0, column=0, pady=3, padx=3, sticky="nsew")

        self.t2 = threading.Thread()
        self.but1 = customtkinter.CTkButton(self, text="Урон", command=self.demageButton)
        self.but1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.but2 = customtkinter.CTkButton(self, text="Хил", command=self.hillButton)
        self.but2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.but5 = customtkinter.CTkButton(self, text='Поглощено', command=self.tankButton)
        self.but5.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

        self.but3 = customtkinter.CTkButton(self, text="TG_Bot", command=self.Tg_Bot_Button)
        self.but3.grid(row=0, column=3, padx=10, pady=10, sticky="nsew", columnspan=1)

        self.but4 = customtkinter.CTkButton(self, text="Переводчик", command=self.transButton)
        self.but4.grid(row=0, column=4, padx=10, pady=10, sticky="nsew", columnspan=1)

    def delbutton(self):
        try:
            name = self.radio.get().rstrip()
            if name != 'Now' and name != '':
                os.remove(f'Archive/ChatBack/{name}')
            self.updateFrame('Trans')

        except FileNotFoundError as f:
            logging.error('Файла для удаления нет', exc_info=True)
            self.updateFrame('Trans')

    def updateFrame(self, title: str):
        defaultFG = '#144870'
        default = '#1f6aa5'
        custom = '#123A59'
        if title == 'Damage':
            self.but2.configure(fg_color=default)
            self.but2.configure(hover_color=defaultFG)

            self.but3.configure(fg_color=default)
            self.but3.configure(hover_color=defaultFG)

            self.but4.configure(fg_color=default)
            self.but4.configure(hover_color=defaultFG)

            self.but5.configure(fg_color=default)
            self.but5.configure(hover_color=defaultFG)

            self.but1.configure(fg_color=custom)
            self.but1.configure(hover_color=custom)

            self.MyDamage.checkbox.ceaftRadio(getSpisok.getSpisok())
            self.MyDamage.my_image.configure(light_image=Image.open('Source\\back.jpg'))
        if title == 'Heal':
            self.but2.configure(fg_color=custom)
            self.but2.configure(hover_color=custom)

            self.but3.configure(fg_color=default)
            self.but3.configure(hover_color=defaultFG)

            self.but4.configure(fg_color=default)
            self.but4.configure(hover_color=defaultFG)

            self.but5.configure(fg_color=default)
            self.but5.configure(hover_color=defaultFG)

            self.but1.configure(fg_color=default)
            self.but1.configure(hover_color=defaultFG)

            self.MyHeal.checkbox.ceaftRadio(getSpisok.getSpisok())
            self.MyHeal.my_image.configure(light_image=Image.open('Source\\back.jpg'))

        if title == 'Tank':
            self.but2.configure(fg_color=default)
            self.but2.configure(hover_color=defaultFG)

            self.but3.configure(fg_color=default)
            self.but3.configure(hover_color=defaultFG)

            self.but4.configure(fg_color=default)
            self.but4.configure(hover_color=default)

            self.but1.configure(fg_color=default)
            self.but1.configure(hover_color=default)

            self.but5.configure(fg_color=custom)
            self.but5.configure(hover_color=custom)

            self.MyTank.checkbox.ceaftRadio(getSpisok.getSpisok())
            self.MyTank.my_image.configure(light_image=Image.open('Source\\back.jpg'))

        if title == 'TG_Bot':
            self.but2.configure(fg_color=default)
            self.but2.configure(hover_color=defaultFG)

            self.but3.configure(fg_color=custom)
            self.but3.configure(hover_color=custom)

            self.but4.configure(fg_color=default)
            self.but4.configure(hover_color=defaultFG)

            self.but5.configure(fg_color=default)
            self.but5.configure(hover_color=defaultFG)

            self.but1.configure(fg_color=default)
            self.but1.configure(hover_color=defaultFG)

            self.MyTgBot.checkbox.sett()
        if title == 'Trans':
            self.but2.configure(fg_color=default)
            self.but2.configure(hover_color=defaultFG)

            self.but3.configure(fg_color=default)
            self.but3.configure(hover_color=defaultFG)

            self.but4.configure(fg_color=custom)
            self.but4.configure(hover_color=custom)

            self.but5.configure(fg_color=default)
            self.but5.configure(hover_color=defaultFG)

            self.but1.configure(fg_color=default)
            self.but1.configure(hover_color=defaultFG)

            self.textbox.delete("1.0", "end")
            self.radio.ceaftRadio([['Now'], ['Now'], [self.getChatList(), self.getChatList()]])
        if title == 'Back':
            self.but2.configure(fg_color=default)
            self.but2.configure(hover_color=defaultFG)

            self.but3.configure(fg_color=default)
            self.but3.configure(hover_color=defaultFG)

            self.but5.configure(fg_color=default)
            self.but5.configure(hover_color=defaultFG)

            self.but4.configure(fg_color=default)
            self.but4.configure(hover_color=defaultFG)

            self.but1.configure(fg_color=default)
            self.but1.configure(hover_color=defaultFG)

            self.MyBack.grid(row=1, column=0, columnspan=5, pady=3, padx=3)

    def demageButton(self):
        logging.info("Вкладка урона")
        if self.activWind == 'Damage':
            self.activWind = 'Back'
            self.MyDamage.grid_forget()
        else:
            self.activWind = 'Damage'
            if self.MyTgBot.winfo_ismapped():
                self.MyTgBot.grid_forget()
            if self.MyHeal.winfo_ismapped():
                self.MyHeal.grid_forget()
            if self.MyTank.winfo_ismapped():
                self.MyTank.grid_forget()
            if self.MyBack.winfo_ismapped():
                self.MyBack.grid_forget()
            if self.MyTrans.winfo_ismapped():
                self.MyTrans.grid_forget()
            if not self.MyDamage.winfo_ismapped():
                self.MyDamage.grid(row=1, column=0, sticky='nsew')
        self.updateFrame(self.activWind)

    def tankButton(self):
        logging.info('Вкладка Танка')
        if self.activWind == 'Tank':
            self.activWind = 'Back'
            self.MyTank.grid_forget()
        else:
            self.activWind = 'Tank'
            if self.MyTgBot.winfo_ismapped():
                self.MyTgBot.grid_forget()
            if self.MyDamage.winfo_ismapped():
                self.MyDamage.grid_forget()
            if self.MyBack.winfo_ismapped():
                self.MyBack.grid_forget()
            if self.MyTrans.winfo_ismapped():
                self.MyTrans.grid_forget()
            if self.MyHeal.winfo_ismapped():
                self.MyHeal.grid_forget()
            if not self.MyTank.winfo_ismapped():
                self.MyTank.grid(row=1, column=0, sticky='nsew')
        self.updateFrame(self.activWind)

    def hillButton(self):
        logging.info("Вкладка Хила")
        if self.activWind == 'Heal':
            self.activWind = 'Back'
            self.MyHeal.grid_forget()
        else:
            self.activWind = 'Heal'
            if self.MyTgBot.winfo_ismapped():
                self.MyTgBot.grid_forget()
            if self.MyDamage.winfo_ismapped():
                self.MyDamage.grid_forget()
            if self.MyBack.winfo_ismapped():
                self.MyBack.grid_forget()
            if self.MyTrans.winfo_ismapped():
                self.MyTrans.grid_forget()
            if self.MyTank.winfo_ismapped():
                self.MyTank.grid_forget()
            if not self.MyHeal.winfo_ismapped():
                self.MyHeal.grid(row=1, column=0, sticky='nsew')
        self.updateFrame(self.activWind)

    def Tg_Bot_Button(self):
        logging.info("Вкладка тг-бота")
        if self.activWind == 'TG_Bot':
            self.activWind = 'Back'
            self.MyTgBot.grid_forget()
        else:
            self.activWind = 'TG_Bot'
            if self.MyDamage.winfo_ismapped():
                self.MyDamage.grid_forget()
            if self.MyHeal.winfo_ismapped():
                self.MyHeal.grid_forget()
            if self.MyBack.winfo_ismapped():
                self.MyBack.grid_forget()
            if self.MyTank.winfo_ismapped():
                self.MyTank.grid_forget()
            if self.MyTrans.winfo_ismapped():
                self.MyTrans.grid_forget()
            if not self.MyTgBot.winfo_ismapped():
                self.MyTgBot.grid(row=1, column=0, sticky='nsew')
        self.updateFrame(self.activWind)

    def transButton(self):
        logging.info("Вкладка переводчика")
        if self.activWind == 'Trans':
            self.activWind = 'Back'
            self.MyTgBot.grid_forget()
        else:
            self.activWind = 'Trans'
            if self.MyDamage.winfo_ismapped():
                self.MyDamage.grid_forget()
            if self.MyHeal.winfo_ismapped():
                self.MyHeal.grid_forget()
            if self.MyTank.winfo_ismapped():
                self.MyTank.grid_forget()
            if self.MyBack.winfo_ismapped():
                self.MyBack.grid_forget()
            if self.MyTgBot.winfo_ismapped():
                self.MyTgBot.grid_forget()
            if not self.MyTrans.winfo_ismapped():
                self.MyTrans.grid(row=1, column=0, sticky='nsew')
        self.updateFrame(self.activWind)

    def getChatList(self):
        if not os.path.exists('Archive/ChatBack'):
            os.mkdir('Archive/ChatBack')
        return os.listdir('Archive/ChatBack')

    def pressChanRadio(self):
        name = self.radio.get()
        if name == 'Now':
            self.activWind = 'Trans'
            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0", self.text_bar)

            if not self.t2.is_alive():
                self.t2 = threading.Thread(target=self.StartLogTrans, args=[self.textbox], daemon=True)
                self.t2.start()

        else:
            self.textbox.delete("1.0", "end")
            x = open(f"Archive\\ChatBack\\{name}", 'r', encoding='utf-8')
            self.textbox.insert("0.0", x.read())

    def StartLogTrans(self, textbox: customtkinter.CTkTextbox):
        try:
            translator = Translator()
            translator.raise_Exception = True
            while self.activWind == 'Trans' and self.ProgaOn:
                with open(f"C:\\Users\\{getpass.getuser()}\\Documents\\ArcheRage\\Chat.log", 'r',
                          encoding='utf-8') as chatLog:
                    ff = chatLog.readlines()
                    try:
                        for i in ff:
                            if self.radio.get() != 'Now':
                                while True:
                                    if self.radio.get() == 'Now':
                                        break
                                    else:
                                        time.sleep(0.15)
                            if not self.ProgaOn:
                                exit()
                            time.sleep(0.3)
                            if self.radio.get() == 'Now':

                                x = translator.translate(i, src='zh-cn', dest='ru').text + '\n'
                                textbox.insert(customtkinter.END, x)
                                self.text_bar += x
                            else:
                                while self.radio.get() != 'Now':
                                    time.sleep(0.15)
                                x = translator.translate(i, src='zh-cn', dest='ru').text + '\n'
                                textbox.insert(customtkinter.END, x)
                                self.text_bar += x
                        f = open(f'C:\\Users\\{getpass.getuser()}\\Documents\\ArcheRage\\Chat.log', 'w',
                                 encoding='utf-8')
                        f.close()

                    except _tkinter.TclError:
                        self.text_bar = ""
                    except Exception as x:
                        logging.error('Ошибка в переводчике', exc_info=True)
        except Exception as e:
            logging.error('Ошибка в переводчике', exc_info=True)


class MyRadiobuttonFrame(customtkinter.CTkScrollableFrame, ):
    def __init__(self, master, title, printBut):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")
        self.spisokradio: dict = {}
        self.printbt = printBut
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

    def ceaftRadio(self, valueVnK):
        self.variable.set('')
        if len(self.spisokradio) == 0:
            for i, value, text in zip([i for i in range(len(valueVnK))], valueVnK[0], valueVnK[1]):
                self.spisokradio[i] = customtkinter.CTkRadioButton(self, text=text, value=value,
                                                                   variable=self.variable,
                                                                   command=self.printbt)
                self.spisokradio[i].grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
        else:
            if len(self.spisokradio) > 0:
                for i in self.spisokradio:
                    self.spisokradio[i].grid_forget()
                    self.spisokradio[i].destroy()
                self.spisokradio = dict()
            for i, value, text in zip([i for i in range(len(valueVnK))], valueVnK[0], valueVnK[1]):
                self.spisokradio[i] = customtkinter.CTkRadioButton(self, text=text, value=value,
                                                                   variable=self.variable,
                                                                   command=self.printbt)
                self.spisokradio[i].grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")

    def get(self):
        return self.variable.get()

    def set(self, valuex):
        self.variable.set(valuex)


class MyMainWindowFrame(customtkinter.CTkFrame):
    def __init__(self, master, title: str, comandUpd):
        super().__init__(master)
        self.comandUpd = comandUpd
        self.grid_columnconfigure(1, weight=1)
        self.leftFr = customtkinter.CTkFrame(self)
        self.leftFr.rowconfigure((0), weight=1)
        self.rightFg = customtkinter.CTkFrame(self)
        self.title = title
        self.checkbox = MyRadiobuttonFrame(self.leftFr, title=title, printBut=self.printBut)
        self.checkbox.grid(row=0, column=0, sticky='nsew')
        self.leftFr.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

        delBut = customtkinter.CTkButton(self.leftFr, text="Удалить", command=self.delbutton)
        delBut.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        rebut = customtkinter.CTkButton(self.leftFr, text="Переименовать", command=self.renBut)
        rebut.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.my_image = customtkinter.CTkImage(light_image=Image.open("Source/back.jpg"), size=(780, 600))
        image_label = customtkinter.CTkLabel(self.rightFg, image=self.my_image, text='')
        self.rightFg.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)
        image_label.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)

    def renBut(self):
        global Id_Dir
        dialog = customtkinter.CTkInputDialog(text="Введите новое название:", title="Переименование")
        x = dialog.get_input()
        if x is not None and x != '' and len(x) > 3:
            name = self.checkbox.get().rstrip()
            Id_Dir[name] = x
            print(Id_Dir)
            with open('Archive\\IdDir.txt', 'w', encoding='utf-8') as idfd:
                json.dump(Id_Dir, idfd)
            self.comandUpd(self.title.strip())

    def delbutton(self):
        global Id_Dir
        try:
            name = self.checkbox.get().rstrip()
            if name != 'Нет записей' and name != '':
                x = os.listdir(f'Archive/Combat/{name}')
                for i in x:
                    os.remove(f'Archive/Combat/{name}/{i}')
                os.rmdir(f'Archive/Combat/{name}')
            Id_Dir = {}
            os.remove('Archive\\IdDir.txt')
            self.comandUpd(self.title.strip())

        except FileNotFoundError as f:
            logging.error('Файла для удаления нет', exc_info=True)
            os.remove('Archive\\IdDir.txt')
            self.comandUpd(self.title.strip())
        except Exception as f:
            print(f)

    def showGraph(self, type, pathD, pathH, pathT):
        try:
            if type == 'Heal':
                self.my_image.configure(light_image=Image.open(pathH))
            if type == 'Damage':
                self.my_image.configure(light_image=Image.open(pathD))
            if type == 'Tank':
                self.my_image.configure(light_image=Image.open(pathT))

        except FileNotFoundError:
            logging.error('Нет файла картинки', exc_info=True)

    def printBut(self):
        if not self.checkbox.get() == 'Нет записей':
            pD, pH, pT = logicMain.AnalyseLogAndDoGraph.goGraph(self.checkbox.get())
            self.showGraph(self.title.strip(), pD, pH, pT)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ArchUt")
        self.geometry("1030x680")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.menuFrame = MyMenuFrame(self)
        self.menuFrame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def ifclosed(self, progOn):
        if not progOn:
            self.menuFrame.ProgaOn = progOn

            self.menuFrame.MyDamage.grid_forget()
            self.menuFrame.MyDamage.destroy()

            self.menuFrame.MyHeal.grid_forget()
            self.menuFrame.MyHeal.destroy()

            self.menuFrame.MyTrans.grid_forget()
            self.menuFrame.MyTrans.destroy()

            self.menuFrame.MyTgBot.grid_forget()
            self.menuFrame.MyTgBot.destroy()
            self.destroy()
            sys.exit()

    def doChatDump(self):
        if len(self.menuFrame.text_bar) > 0:
            now = datetime.datetime.now()
            name = now.strftime("%d %b %Hч %Mм %Sс")
            x = open(f'Archive\\ChatBack\\[{name}]', 'w', encoding='utf-8')
            x.write(self.menuFrame.text_bar)
            x1 = open(f"C:\\Users\\{getpass.getuser()}\\Documents\\ArcheRage\\Chat.log", 'w')
            x1.close()

    def rrrr(self):
        self.menuFrame.activWind = None
