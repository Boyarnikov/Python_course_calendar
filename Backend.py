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
import datetime as dt


class Backend:

    @staticmethod
    def write_event(data, name_csv):
        with open(f'data_base/{name_csv}.csv', 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['date', 'name', 'description'])
            w.writerow(data)
        input('=' * 37 + '\n'
                         f'Событие "{data.get("name")}" добавлено! для продолжения нажмите Enter')

    @staticmethod
    def events_from_csv(name_csv):
        with open(f'data_base/{name_csv}.csv', 'r') as f:
            r = csv.DictReader(f, fieldnames=['date', 'name', 'description'])
            list_events = ['Мероприятия:\n']
            # print(list(r))
            for n in r:
                if n['name'] == 'name':
                    continue
                d = dt.datetime.fromtimestamp(int(n['date'])).strftime('%d-%m-%Y')
                list_events.append(f"Дата: {d}\n"
                                   f"Название: {n['name']}\n"
                                   f"Описание: {n['description']}\n\n")
        return list_events if len(list_events) > 1 else 'У Вас нет запланированных мероприятий!\n'

    @staticmethod
    def add_user_bk(name, pwd):
        if 'domains.csv' not in os.listdir('./data_base'):
            with open('data_base/domains.csv', 'x', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['name', 'pwd'])
                w.writeheader()
                w.writerow({'name': name, 'pwd': pwd})
        else:
            with open('data_base/domains.csv', 'a', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['name', 'pwd'])
                w.writerow({'name': name, 'pwd': pwd})
        with open(f'data_base/{name}.csv', 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['date', 'name', 'description'])
            w.writeheader()

    @staticmethod
    def check_user_domain(name):
        if 'domains.csv' not in os.listdir('./data_base'):
            return True
        with open('data_base/domains.csv', 'r') as f:
            r = csv.DictReader(f, fieldnames=['name'])
            for n in r:
                if n['name'][1:] == name:
                    return False
            return True

    @staticmethod
    def check_user_pwd(name, pwd):
        with open('data_base/domains.csv', 'r') as f:
            r = csv.DictReader(f, fieldnames=['name', 'pwd'])
            for n in r:
                if n['name'] == name and n['pwd'] == pwd:
                    return True
            return False
