"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
import datetime
import Backend


class Calendar:
    __state_machin = {'date': 0, 'name': '', 'description': ''}
    _bk = Backend.Backend()

    def _date_state(self):
        result = input("Введите дату события в формате dd-mm-yyyy\n"
                       "Завершить работу программы: '0'\n").split('-')
        if result == '0':
            exit()
        elif all(map(lambda x: x.isdigit(), result)):
            self.__state_machin['date'] = int(datetime.datetime.strptime('-'.join(result), '%d-%m-%Y').timestamp())
            self._name_state()
        else:
            print('не корректный ввод')
            self._date_state()

    def _name_state(self):
        result = input("Введите названия события\n"
                       "Завершить работу программы: '0'\n")
        self.__state_machin['name'] = result
        self._descr_state()

    def _descr_state(self):
        result = input("Введите краткое описание\n"
                       "Завершить работу программы: '0'\n")
        self.__state_machin['description'] = result
        self._bk.write_to_csv(self.__state_machin)

    def add_event(self):
        self._date_state()

    def get_events(self):
        pass
