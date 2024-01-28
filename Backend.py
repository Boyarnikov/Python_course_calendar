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
            return list(csv.DictReader(f, fieldnames=['date', 'name', 'description']))

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

    @staticmethod
    def del_event_csv(name_csv, date):
        with open(f'data_base/{name_csv}.csv', 'r') as f:
            r = csv.DictReader(f, fieldnames=['date', 'name', 'description'])
            new_r = []
            for i in r:
                _d = {}
                if i['date'] == str(date) or i['date'] == 'date':
                    continue
                _d['date'] = i['date']
                _d['name'] = i['name']
                _d['description'] = i['description']
                new_r.append(_d)

        with open(f'data_base/{name_csv}.csv', 'w') as f:
            w = csv.DictWriter(f, fieldnames=['date', 'name', 'description'])
            w.writeheader()
            for row in new_r:
                w.writerow(row)
