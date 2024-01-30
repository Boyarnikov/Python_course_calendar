"""
Описывает некоторе "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданым
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""
import json

from Backend import Backend


class Event:
    date_event = None
    name_event = None
    description = None
    organizer = None
    set_data = None
    name_user = None
    participants = None

    def __init__(self, data, name_user, org_name):
        self.date_event = data['date']
        self.name_event = data['name']
        self.description = data['description']
        self.participants = data['participants']
        self.organizer = org_name
        self.name_user = name_user
        self.set_data = {name_user: data}

    def set_json_to_bk(self):
        d_j = json.dumps(self.set_data)
        Backend.write_event(d_j)

