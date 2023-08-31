x = (
    '[08/30/23 10:57:08] Оствинд|r атакует. Ужасающая абоминация|r получает |cffff0000критический урон|r. |cffff0000Здоровье|r снижается на |cffff0000-1007|r ед.')
z = x.split('cffff0000')
if 'Поглощено' in x:
    if 'блокирует' in x:
        print(x.split('|r')[2][3:])
        print(int(x.split('|r')[-1].split()[3]) + abs(int(z[3].split('|r')[0])))

    else:
        print(x.split('|r')[2][3:])
        print(int(x.split('|r')[-1].split()[2]) + abs(int(z[3].split('|r')[0])))

elif 'блокирует' in x:
    print(x.split('|r')[2][3:])
    print(abs(int(z[1].split('|r')[0])))  # Блок
else:
    if 'атакует' in x:
        print(x.split('|r')[1].split('атакует.')[1].strip())
    else:
        print(x.split('|r')[2][3:])
        print(abs(int(z[3].split('|r')[0])))  # Дефолт

