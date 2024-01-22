"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""


import datetime
import calendar
from colorama import Fore
import subprocess
import math


class Interface:
    __DICT_MONTH = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май',
                    6: 'Июнь', 7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь',
                    11: 'Ноябрь', 12: 'Декабрь'}
    __DAYS_WEEK = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')
    __state_machin = None
    _func_queue = []

    @staticmethod
    def create_monthcalendar(year, month):
        start_days, count_days = calendar.monthrange(year, month)
        gen_monthcalendar = [' ' if i < start_days else i - start_days for i in range(1, count_days + start_days + 1)]
        days_list = [[' ' for _ in range(7)] for _ in range(math.ceil(len(gen_monthcalendar) / 7))]
        for i, j in enumerate(gen_monthcalendar):
            if j == 0:
                j = ' '
            days_list[i // 7][i % 7] = j
        return days_list

    @staticmethod
    def show_calendar(m=0, y=0):
        subprocess.call('clear')  # очистить терминал MacOs, windows 'cls'
        year: int = datetime.datetime.now().year + y
        month_current: int = datetime.datetime.now().month + m
        day_now: int = datetime.datetime.now().day if month_current == datetime.datetime.now().month else None
        if month_current < 1:
            year, month_current = year - 1, 12
        if month_current > 12:
            year, month_current = year + 1, 1
        month = Interface.__DICT_MONTH.get(month_current)
        print('<< |', str(year).center(22), '| >>')
        print(*Interface.__DAYS_WEEK, sep=' | ')
        num_days = Interface.create_monthcalendar(year, month_current)
        for week in num_days:
            for day in week:
                if day == day_now:
                    print(Fore.BLUE + str(day).rjust(2) + Fore.RESET, end=' | ')
                else:
                    print(str(day).rjust(2), end=' | ')
            print('')
        print('<  |', month.center(22), '|  >')
        Interface.state_start(m, y)

    @staticmethod
    def state_start(m, y):
        result = input('''
Поменять месяц введите: '<' или '>'
Поменять год введите: '<<' или '>>'
Добавить мероприятие введите: 'add'
Завершить работу программы: '0'
''')
        if result == '<':
            Interface._func_queue.append(Interface.show_calendar(m=-1 + m))
        elif result == '>':
            Interface._func_queue.append(Interface.show_calendar(m=1 + m))
        elif result == '0':
            exit()

    @staticmethod
    def start():
        Interface._func_queue.append(Interface.show_calendar())
        while Interface._func_queue:
            Interface._func_queue[0]()
            del Interface._func_queue[0]
        print('Календарь закончил работу!')
        exit()


interface_start = Interface()
interface_start.start()

