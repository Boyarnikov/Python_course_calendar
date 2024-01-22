"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.
"""
import csv
import os


class Backend:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def write_to_csv(data):
        if 'events.csv' not in os.listdir('./data_base'):
            with open('data_base/events.csv', 'x') as f:
                w = csv.DictWriter(f, fieldnames=['date', 'name', 'description'])
                w.writeheader()
                w.writerow(data)
        else:
            with open('data_base/events.csv', 'a') as f:
                w = csv.DictWriter(f, fieldnames=['date', 'name', 'description'])
                w.writerow(data)
        input('=' * 37 + '\n'
                         f'Событие "{data.get("name")}" добавлено! для продолжения нажмите Enter')
