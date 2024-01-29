"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
import datetime
import re

import Backend
import Event


class Calendar:
    __data_state = {'date': 0, 'name': '', 'description': ''}
    __state_machin = None
    _bk = Backend.Backend()
    _name_user = ''

    def _name_state(self):
        self.__state_machin = 'name'
        result = input("Введите названия события:\n")

        self.__data_state[self.__state_machin] = result
        self._descr_state()

    def _date_state(self):
        date_regular = r'^\d{2}-\d{2}-\d{4}$'
        self.__state_machin = 'date'
        result = input("Введите дату события в формате: dd-mm-yyyy\n"
                       "Завершить работу программы: 0\n")
        if re.match(date_regular, result):
            result = result.split('-')
        if all(map(lambda x: x.isdigit(), result)):
            self.__data_state[self.__state_machin] = int(
                datetime.datetime.strptime('-'.join(result), '%d-%m-%Y').timestamp())
            self._name_state()
        elif result == '0':
            pass
        else:
            print('не корректный ввод')
            self._date_state()

    def _descr_state(self):
        self.__state_machin = 'description'
        result = input("Введите краткое описание:\n")
        self.__data_state[self.__state_machin] = result
        self._ev = Event.Event(data=self.__data_state, name_user=self._name_user)
        self._ev.set_json_to_bk()


    def add_event(self, name):
        self._name_user = name
        self._date_state()

    def get_events(self, name):
        return self._bk.events_from_csv(name_csv=name)

    def del_event(self, name, event: str):
        date: str = event.split('\n')[1].split()[1]
        ds: int = int(datetime.datetime.strptime(date, '%d-%m-%Y').timestamp())
        self._bk.del_event_csv(name_csv=name, date=ds)

    def get_name_event(self):
        return self._ev.name_event
