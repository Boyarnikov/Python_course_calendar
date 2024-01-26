"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""

import datetime as dt
import calendar
from colorama import Fore
import subprocess
import math
import numpy as np
from getpass import getpass
import time

import Calendar
import User
import Backend


class Interface:
    __DICT_MONTH = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май',
                    6: 'Июнь', 7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь',
                    11: 'Ноябрь', 12: 'Декабрь'}
    __DAYS_WEEK = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')
    _func_queue = []
    _calendar = Calendar.Calendar()
    _user = User.User()
    _count_m = 0
    _count_y = 0
    _bk = Backend.Backend()

    @staticmethod
    def clear_window():
        subprocess.call('clear')  # очистить терминал MacOs, windows 'cls'

    @staticmethod
    def create_monthcalendar(year, month):
        start_days, count_days = calendar.monthrange(year, month)
        gen_monthcalendar = [0 if i < start_days else i - start_days for i in range(1, count_days + start_days + 1)]
        # days_list = [[' ' for _ in range(7)] for _ in range(math.ceil(len(gen_monthcalendar) / 7))]       #  if not have numpy
        days_list = np.zeros((math.ceil(len(gen_monthcalendar) / 7), 7), dtype=object)
        for i, j in enumerate(gen_monthcalendar):
            if j == 0:
                j = ' '
            days_list[i // 7][i % 7] = j
        return days_list

    # @staticmethod
    def show_calendar(self):
        Interface.clear_window()
        year_now = dt.datetime.now().year
        month = dt.datetime.now().month
        y = self._count_m // 12 + self._count_y
        month_int: int = month + self._count_m % 12
        year: int = year_now + y
        # days_months = sum([calendar.monthrange(year, i)[1] for i in range(month, month_int)])
        day_now: int = dt.datetime.now().day if month == month_int and year_now == year else None  # (today + dt.timedelta(days=days_months)) == today
        month = self.__DICT_MONTH.get(month_int)

        print('<< |', str(year).center(22), '| >>')
        print(*Interface.__DAYS_WEEK, sep=' | ')

        num_days = Interface.create_monthcalendar(year, month_int)
        for week in num_days:
            for day in week:
                if day == day_now:
                    print(Fore.BLUE + str(day).rjust(2) + Fore.RESET, end=' | ')
                else:
                    print(str(day).rjust(2), end=' | ')
            print('')
        print('<  |', month.center(22), '|  >')
        self._func_queue.append(self.state_start)

    # @staticmethod
    def state_start(self):
        result = input('''
Изменить месяц введите: '<' или '>'
Изменить год введите: '<<' или '>>'
Добавить мероприятие введите: add
Завершить работу программы: 0
''')
        if result == '<':
            self._count_m -= 1
            Interface._func_queue.append(self.show_calendar)
        elif result == '>':
            self._count_m += 1
            self._func_queue.append(self.show_calendar)
        elif result == '<<':
            self._count_y -= 1
            self._func_queue.append(self.show_calendar)
        elif result == '>>':
            self._count_y += 1
            self._func_queue.append(self.show_calendar)
        elif result == 'add':
            self._calendar.add_event()
            self._func_queue.append(Interface.show_calendar)
        elif result == '0':
            pass
        else:
            raise ValueError('не допустимое значение ввода!')

    def state_enter(self):
        result = input('=' * 37 + '\n'
                                  'Пробывать еще раз: try\n'
                                  'Для регистрации нового аккаунта введите: reg\n'
                                  'Завершить работу программы: 0\n')
        if result == 'try':
            self._func_queue.append(self.run_enter)
        elif result == 'reg':
            self._func_queue.append(self.run_reg)
        elif result == '0':
            pass
        else:
            raise ValueError('не допустимые значения ввода')

    def run_welcome(self):
        print('\n'
              'Добро пожаловать в программу Календарь!\n'
              'С помощью данной программы вы сможете легко и непринуждённо планировать свои дела!')
        result = input('=' * 37 + '\n'
                                  'Если у Вас есть аккаунт для входа нажмите Enter\n'
                                  'Для регистрации нового аккаунта введите: reg\n')
        if result == 'reg':
            self._func_queue.append(self.run_reg)
        else:
            self.run_enter()

    def run_enter(self):
        _name = input('Введите имя пользователя: ')
        if self._bk.check_user_domain(name=_name) is False:
            _pwd = getpass('Введитре пароль: ')
            self._user.create_user(_name, _pwd)
            _name, _pwd = (self._user.get_name(), self._user.get_hash_pwd())
            if self._bk.check_user_pwd(name=_name, pwd=_pwd):
                self._func_queue.append(self.show_calendar)
            else:
                print(f'Неверный пароль!')
                self.state_enter()
        else:
            print(f'Пользователя с именем "{_name}" нет!')
            self.state_enter()

    def run_reg(self):
        name = input('Введите имя пользователя: ')
        if self._bk.check_user_domain(name=name):
            while True:
                pwd = getpass('Введитре пароль: ')
                pwd2 = getpass('Повторите пароль: ')
                if pwd == pwd2:
                    break
                else:
                    print('Пароли не совпадают! попробуйте еще раз')
            self._user.create_user(name=name, pwd=pwd)
            self._func_queue.append(self.add_user)
        else:
            print('!Пользователь с таким именем уже существует!\n'
                  'Введите другое имя')
            self._func_queue.append(self.run_reg)

    def add_user(self):
        _name = self._user.get_name()
        self._bk.add_user_bk(_name, self._user.get_hash_pwd())
        Interface.clear_window()
        print(f'Аккаунт с именем: {_name} создан!')
        time.sleep(2)
        self._func_queue.append(self.show_calendar)

    # @staticmethod
    def start(self):
        self._func_queue.append(self.run_welcome)  # run_enter
        while self._func_queue:
            self._func_queue[0]()
            del self._func_queue[0]
        print('Календарь закончил работу!!!')
        exit()


interface_start = Interface()
interface_start.start()
