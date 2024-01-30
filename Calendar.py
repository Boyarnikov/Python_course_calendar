"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
import datetime
import re
import time

import Backend
import Event


class Calendar:
    __data_state = {'date': 0,
                    'name': '',
                    'description': '',
                    'organizer': '',
                    'participants': None}

    __state_machin = None
    _bk = Backend.Backend()
    _name_user = ''
    _ev = None

    def _name_state(self):
        self.__state_machin = 'name'
        result = input("Введите названия события:\n")
        if result:
            self.__data_state[self.__state_machin] = result
            self._descr_state()
        else:
            print('Название не может быть пустым!')
            self._name_state()

    def _date_state(self):
        date_regular = r'^\d{2}-\d{2}-\d{4}$'
        self.__state_machin = 'date'
        result = input("Введите дату события в формате: dd-mm-yyyy\n"
                       "Завершить работу программы: 0\n").replace(' ', '')
        if len(result) == 10:
            if re.match(date_regular, result):
                result = result.split('-')
            if all(map(lambda x: x.isdigit(), result)):
                self.__data_state[self.__state_machin] = int(
                    datetime.datetime.strptime('-'.join(result), '%d-%m-%Y').timestamp())
                self._name_state()
        elif result == '0':
            exit()
        else:
            print('не корректный ввод')
            self._date_state()

    def _descr_state(self):
        self.__state_machin = 'description'
        result = input("Введите краткое описание:\n")
        self.__data_state[self.__state_machin] = result
        result = input('Хотите ли Вы добавить участников y/n: ')
        if result == 'y':
            self._participants_state()
        elif result == 'n':
            self.set_to_csv(self._name_user)
        else:
            raise ValueError('Недопустимый ввод!')

    def _participants_state(self):
        self.__state_machin = 'participants'
        names = self._bk.get_users(self._name_user)
        print('Имена:')
        print(*names)
        result = input('Введите номера участников через пробел: ').split()
        participants_set = set()
        if all(map(lambda x: x.isdigit(), result)):
            for i in result:
                try:
                    participants_set.add(names[int(i) - 1].split()[-1][:-1])
                except IndexError:
                    print(f'Значение {i} не корректно!!!')
            self.__data_state[self.__state_machin] = list(participants_set)

            self.set_to_csv(name_user=self._name_user)

            if participants_set:
                for name in participants_set:
                    self.set_to_csv(name_user=name)

    def set_to_csv(self, name_user):
        self._ev = Event.Event(data=self.__data_state, name_user=name_user, org_name=self._name_user)
        self._ev.set_json_to_bk()

    def add_event(self, name):
        self._name_user = name
        self.__data_state['organizer'] = name
        self._date_state()

    def get_events(self, name):
        return self._bk.events_from_csv(name_csv=name)

    def del_event(self, name, event: str):
        date: str = event.split('\n')[1].split()[1]
        ds: int = int(datetime.datetime.strptime(date, '%d-%m-%Y').timestamp())
        res = self._get_organizer_participants(name_csv=name, date=ds)
        if res['organizer'] == name:
            self._bk.del_event_csv(name_csv=name, date=ds)
            list_participants = \
                res['participants'].replace("[", "").replace("]", "").replace("'", "").replace('"', '').replace(',', '')
            list_participants = list_participants.split()
            if list_participants:
                for name in list_participants:
                    self._bk.del_event_csv(name_csv=name, date=ds)
        else:
            print('Вы не можете удалить это мероприятие, вы не являетесь его организатором! ')
            time.sleep(1.7)

    def _get_organizer_participants(self, name_csv, date):
        return self._bk.get_event(name_csv, date)

    def get_name_event(self):
        return self._ev.name_event
