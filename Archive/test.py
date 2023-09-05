import time
from datetime import date
import json

"""""'АГЛ(JMG)', 'Кровь', 'Призрачка',
'Анталон',
'Новый день', 'Лицензии', 'Вексели', 'Порт-Аргенто', 'Библиотека',
'Дейлики',
'Даскшир', 'Гартрейн', 'Мечи: Запад', 'Мечи: Восток', 'Эфен',
'Бухта',
'Паки', 'Аукцион', 'Друг онлайн', 'Кирка',
'Мирка-Cевер', 'Спруты', 'Око бури', 'Осада', 'Ксанатос',
'Дельфиец',
'Кракен',
'Левиафан'"""""

print(date.today().day)
DefaultDay = {'DATEDAY': date.today().day, 'АГЛ(JMG)': True, 'Кровь': True, 'Призрачка': True, 'Анталон': True,
              'Лицензии': True, 'Вексели': True, 'Порт-Аргенто': True, 'Библиотека': True,
              'Дейлики': True, 'Эфен': True, 'Бухта': True, 'Даскшир': True, 'Гартрейн': True, 'Мечи: Запад': True,
              'Мечи: Восток': True, 'Спруты': True, "Рубеж":True,}
with open('DumpDay.txt', 'w+', encoding='utf-8') as file:
    json.dump(not DefaultDay, file)
    time.sleep(2)
x = open('DumpDay.txt', 'r', encoding='utf-8')
ff = x.read()
print(z := json.loads(ff))
