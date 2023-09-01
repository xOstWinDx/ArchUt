# -*- coding: utf-8 -*-
import os.path
import json
import matplotlib.pyplot as plt
import matplotlib

import logging
if not os.path.exists('loggs'):
    os.mkdir('loggs')
logging.basicConfig(level=logging.INFO, filename="loggs\\ArchUt.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class AnalyseLogAndDoGraph:
    matplotlib.use('agg')

    @staticmethod
    def DoHealAndDamage(name: str):
        if not os.path.exists(fr'Archive\Combat\{name}\Damage_{name}.txt') and not os.path.exists(
                fr'Archive\Combat\{name}\Heal_{name}.txt'):
            try:
                with open(fr"Archive\Combat\{name}\Комбо_{name}_Рейд.log", "r", encoding='utf-8') as file:
                    hill_dict = dict()
                    damage_dict = dict()
                    tank_dict = dict()
                    wewe = file.readlines()

                    for i in wewe:
                        d = i
                        if 'восстанавливает' in i and 'маны' not in i:
                            if i[20:i.index('|r')] not in hill_dict:
                                hill_dict[i[20:i.index('|r')]] = 0
                            hill_dict[i[20:i.index('|r')]] += int(i[i.index('cff00ff00') + 9:-17])
                        if 'снижается на' in i:
                            if 'Поглощено' in i:
                                d = i[:i.rindex('|r') + 7]
                                if d.find('cffff0000-') == -1:
                                    print(i)
                                    pass
                            else:
                                if d[20:d.index('|r')] not in damage_dict:

                                    damage_dict[d[20:d.index('|r')]] = 0
                                damage_dict[d[20:d.index('|r')]] += int(d[d.index('cffff0000-') + 10:-7])
                                z = i.split('cffff0000')

                            if 'Поглощено' in i:
                                if 'блокирует' in i:
                                    if i.split('|r')[2][3:] in tank_dict:
                                        if int(i.split('|r')[-1].split()[3]) + abs(int(z[3].split('|r')[0])) > 25000:
                                            tank_dict[i.split('|r')[2][3:]] += 6000
                                        else:
                                            tank_dict[i.split('|r')[2][3:]] += int(i.split('|r')[-1].split()[3]) + abs(
                                                int(z[3].split('|r')[0]))
                                    else:
                                        if int(i.split('|r')[-1].split()[3]) + abs(int(z[3].split('|r')[0])) > 20000:
                                            tank_dict[i.split('|r')[2][3:]] = 6000
                                        else:
                                            tank_dict[i.split('|r')[2][3:]] = int(i.split('|r')[-1].split()[3]) + abs(
                                                int(z[3].split('|r')[0]))

                                else:
                                    if i.split('|r')[2][3:] in tank_dict:
                                        tank_dict[i.split('|r')[2][3:]] += int(i.split('|r')[-1].split()[2]) + abs(
                                            int(z[3].split('|r')[0]))

                            elif 'блокирует' in i:
                                if i.split('|r')[2][3:] in tank_dict:
                                    if abs(int(z[1].split('|r')[0])) > 30000:
                                        tank_dict[i.split('|r')[2][3:]] += 4000
                                    else:
                                        tank_dict[i.split('|r')[2][3:]] += abs(int(z[1].split('|r')[0]))
                                else:
                                    if abs(int(z[1].split('|r')[0])) > 30000:
                                        tank_dict[i.split('|r')[2][3:]] = 4000
                                    else:
                                        tank_dict[i.split('|r')[2][3:]] = abs(int(z[1].split('|r')[0]))  # Блок
                            else:

                                if 'атакует' in i:
                                    if i.split('|r')[1].split('атакует.')[1].strip() in tank_dict:
                                        if abs(int(z[3].split('|r')[0])) > 30000:
                                            tank_dict[i.split('|r')[1].split('атакует.')[1].strip()] += 5000
                                        else:
                                            tank_dict[i.split('|r')[1].split('атакует.')[1].strip()] += abs(
                                                int(z[3].split('|r')[0]))
                                    else:
                                        if abs(int(z[3].split('|r')[0])) > 30000:
                                            tank_dict[i.split('|r')[1].split('атакует.')[1].strip()] = 5000
                                        else:
                                            tank_dict[i.split('|r')[1].split('атакует.')[1].strip()] = abs(
                                                int(z[3].split('|r')[0]))
                                else:
                                    if i.split('|r')[2][3:] in tank_dict:
                                        if abs(int(z[3].split('|r')[0])) > 30000:
                                            tank_dict[i.split('|r')[2][3:]] += 5000
                                        else:
                                            tank_dict[i.split('|r')[2][3:]] += abs(int(z[3].split('|r')[0]))
                                    else:
                                        # print(i)
                                        if abs(int(z[3].split('|r')[0])) > 30000:
                                            tank_dict[i.split('|r')[2][3:]] = 5000
                                        else:
                                            tank_dict[i.split('|r')[2][3:]] = abs(int(z[3].split('|r')[0]))

                    if len(tank_dict) > 25:
                        ogrv = 45000
                        for tvalue in list(tank_dict.keys()):
                            if len(tank_dict) > 33:
                                ogrv = 70000
                            if tank_dict[tvalue] < ogrv:
                                del tank_dict[tvalue]
                            if len(tvalue) > 15 and tvalue in tank_dict:
                                del tank_dict[tvalue]

                    if len(damage_dict) > 25:
                        for dvalue in list(damage_dict.keys()):
                            if damage_dict[dvalue] < 15000:
                                del damage_dict[dvalue]
                            if len(dvalue) > 15 and dvalue in damage_dict:
                                del damage_dict[dvalue]
                    if len(hill_dict) > 25:
                        for hvalue in list(hill_dict.keys()):
                            if hill_dict[hvalue] < 15000:
                                del hill_dict[hvalue]
                    z = sorted(tank_dict, key=lambda t: tank_dict[t], reverse=True)
                    y = sorted(damage_dict, key=lambda k: damage_dict[k], reverse=True)

                    if len(z) > 10:
                        maxtank = list([z[3], tank_dict[z[3]]])
                        for tvalue in z:
                            if tank_dict[tvalue] * 15 < maxtank[-1]:
                                del tank_dict[tvalue]
                    if len(y) > 5:
                        maxDamage = list([y[2], damage_dict[y[2]]])
                        for dvalue in y:
                            if damage_dict[dvalue] * 20 < maxDamage[-1]:
                                del damage_dict[dvalue]
                    y = sorted(damage_dict, key=lambda k: damage_dict[k], reverse=False)
                    y2 = sorted(hill_dict, key=lambda k: hill_dict[k], reverse=False)
                    z2 = sorted(tank_dict, key=lambda k: tank_dict[k], reverse=False)

                    sortDamageDic = {}
                    sortHealDic = {}
                    sortTankDict = {}

                    for i in y:
                        sortDamageDic[i] = damage_dict[i]
                    for i in y2:
                        sortHealDic[i] = hill_dict[i]
                    for i in z2:
                        sortTankDict[i] = tank_dict[i]

                    fff = open(f"Archive\\Combat\\{name}\\Damage_{name}.txt", 'w', encoding='utf-8')
                    fff2 = open(f"Archive\\Combat\\{name}\\Heal_{name}.txt", 'w', encoding='utf-8')
                    fff3 = open(f"Archive\\Combat\\{name}\\Tank_{name}.txt", 'w', encoding='utf-8')

                    json.dump(sortDamageDic, fff)
                    json.dump(sortHealDic, fff2)
                    json.dump(sortTankDict, fff3)

                fff.close()
                fff2.close()
                fff3.close()

            except FileNotFoundError:
                logging.error("Что-то с файлом комбо рейда")

    @staticmethod
    def goGraph(name: str):
        print(name)
        name = name.rstrip()
        pathZ = 'Source/NoData.png'
        pathD = 'Source/NoData.png'
        pathH = 'Source/NoData.png'
        pathT = 'Source/NoData.png'

        def human_format(num):
            num = float('{:.3g}'.format(num))
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

        font = {'color': 'Lavender',
                'weight': 'bold',
                'size': 5
                }
        try:
            with open(f'Archive\\Combat\\{name}\\Damage_{name}.txt', encoding='utf-8') as damage:
                strip = damage.read().lstrip()
                if len(strip) > 3:
                    dics = json.loads(strip)
                    y, x = list(dics.keys()), list(map(int, dics.values()))
                    logging.info('Прочитал файл урона')
                else:
                    y, x = 0, 0
                    pathD = pathZ

            if x != 0:
                if not os.path.exists(f'Archive\\Combat\\{name}\\Damage_{name}.png'):
                    plt.rcParams.update(
                        {'font.size': 6, 'font.weight': 'bold', 'ytick.color': '#61b1d4ec',
                         'figure.facecolor': '#212121',
                         'axes.edgecolor': '#212121'})

                    ax = plt.axes()
                    ax.set_facecolor('#212121')
                    #ff3030  IndianRed #fe3030
                    plt.barh(y, x, color='#fe3030', align='center', capstyle='projecting', height=0.4)
                    for index, value in enumerate(x):
                        plt.text(value, index,
                                 human_format(value), fontdict=font)

                    plt.tight_layout(pad=0.05)
                    plt.xticks([])

                    plt.savefig(f'Archive\\Combat\\{name}\\Damage_{name}.png', dpi=250, bbox_inches='tight',
                                orientation='portrait', pad_inches=0)
                    plt.close()
                    pathD = f'Archive\\Combat\\{name}\\Damage_{name}.png'
                else:
                    pathD = f"Archive\\Combat\\{name}\\Damage_{name}.png"
                logging.info("Создал график урона")
        except FileNotFoundError:
            logging.error("Файла нет в папке", exc_info=True)

        try:
            with open(f'Archive\\Combat\\{name}\\Heal_{name}.txt', encoding='utf-8') as Heal:
                strip = Heal.read()
                if len(strip) > 3:
                    dics = json.loads(strip)

                    y2, x2 = list(dics.keys()), list(map(int, dics.values()))
                    logging.info('Прочитал текст Хила')
                else:
                    y2, x2 = 0, 0
                    print("тут")
                    pathH = pathZ
            if x2 != 0:
                if not os.path.exists(f'Archive\\Combat\\{name}\\Heal_{name}.png'):
                    plt.rcParams.update(
                        {'font.size': 6, 'font.weight': 'bold', 'ytick.color': '#61b1d4ec',
                         'figure.facecolor': '#212121',
                         'axes.edgecolor': '#212121'})

                    ax = plt.axes()
                    ax.set_facecolor('#212121')
                    #30ff45 PaleGreen 30ff6b
                    plt.barh(y2, x2, color='#30ff6b', align='center', capstyle='projecting', height=0.4)

                    for index, value in enumerate(x2):
                        plt.text(value, index,
                                 human_format(value), fontdict=font)

                    plt.tight_layout(pad=0.05)
                    plt.xticks([])

                    plt.savefig(f'Archive\\Combat\\{name}\\Heal_{name}.png', dpi=250, bbox_inches='tight',
                                orientation='portrait', pad_inches=0)
                    plt.close()
                    pathH = f'Archive\\Combat\\{name}\\Heal_{name}.png'
                else:
                    pathH = f'Archive\\Combat\\{name}\\Heal_{name}.png'
        except FileNotFoundError:
            logging.error('Файла нет', exc_info=True)

        try:
            with open(f'Archive\\Combat\\{name}\\Tank_{name}.txt', encoding='utf-8') as Tank:
                strip = Tank.read()
                if len(strip) > 3:
                    dics = json.loads(strip)

                    y2, x2 = list(dics.keys()), list(map(int, dics.values()))
                    logging.info('Прочитал текст танка')
                else:
                    y2, x2 = 0, 0
                    pathT = pathZ
            if x2 != 0:
                if not os.path.exists(f'Archive\\Combat\\{name}\\Tank_{name}.png'):
                    plt.rcParams.update(
                        {'font.size': 6, 'font.weight': 'bold', 'ytick.color': '#61b1d4ec',
                         'figure.facecolor': '#212121',
                         'axes.edgecolor': '#212121'})

                    ax = plt.axes()
                    ax.set_facecolor('#212121')
                        #ff6d2e ffe561
                    plt.barh(y2, x2, color='#ff6d2e', align='center', capstyle='projecting', height=0.4)

                    for index, value in enumerate(x2):
                        plt.text(value, index,
                                 human_format(value), fontdict=font)

                    plt.tight_layout(pad=0.05)
                    plt.xticks([])

                    plt.savefig(f'Archive\\Combat\\{name}\\Tank_{name}.png', dpi=250, bbox_inches='tight',
                                orientation='portrait', pad_inches=0)
                    plt.close()
                    pathT = f'Archive\\Combat\\{name}\\Tank_{name}.png'
                else:
                    pathT = f'Archive\\Combat\\{name}\\Tank_{name}.png'
        except FileNotFoundError:
            logging.error('Файла нет', exc_info=True)

        return pathD, pathH, pathT
