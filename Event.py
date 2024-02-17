"""
Описывает некоторoе "событие" - промежуток времени с присвоенными характеристиками
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
import re
import json
import datetime
from dateutil import rrule
from User import User
import json

class Event:
    def __init__(self, title, organizer, description=None, participants=None, frequency=None):
        self._title = title
        self._organizer = organizer
        self._description = description
        self._participants = participants if participants is not None else set()
        if isinstance(organizer, User):
            self._participants.add(organizer)
        self._frequency = frequency if frequency is not None else []

        
    def __repr__(self):
        return f"('{self._title}',организатор: {self._organizer}, участники: {self._participants}, описание: {self._description}, даты проведения: {self._frequency})"
    
    def __eq__(self, other):
        if isinstance(other, Event):
            return (self._title == other._title and self._organizer == other._organizer)
        return False
    
    def __hash__(self):
        return hash((self._title, self._organizer))
    
    def get_title(self):
        return self._title
    
    def get_organizer(self):
        return self._organizer
    
    def get_participants(self):
        return self._participants
    
    def get_description(self):
        return self._description
    
    def get_frequency_event(self):
        return self._frequency
    
    def create_periodic_event(self, start_date, frequency, format = "%Y-%m-%d"):
        '''Метод задает частоту события на 5 лет вперед начиная с установленной даты первого события.'''
        if isinstance(start_date, datetime.date):
            start_date = start_date.strftime(format)
        start_date = datetime.datetime.strptime(start_date, format)
        end_date = start_date + datetime.timedelta(days=365 * 5)
        if frequency == "once":
            self._frequency.append(start_date)
        else:
            if frequency == "daily":
                rule = rrule.DAILY
            elif frequency == "weekly":
                rule = rrule.WEEKLY
            elif frequency == "monthly":
                rule = rrule.MONTHLY
            elif frequency == "yearly":
                rule = rrule.YEARLY
            else:
                print("Неверные данные.")
                return
            for date in rrule.rrule(rule, dtstart=start_date, until=end_date):
                self._frequency.append(date)
                
    def add_part(self, admin, participant):
        '''Добавление участников события.'''
        if admin == self._organizer and isinstance(admin, User) and isinstance(participant, User):
            self._participants.add(participant)
            participant.notify_added_to_event(self)
        else:
            print("Введены некоректные данные")
            # raise ValueError("Некорректные участники события.")

    def del_participants(self,event_name, admin, user):
        '''Удаление участников события.'''
        if admin == self._organizer and event_name == self._title and user in self._participants and user != self._organizer :
            self._participants.remove(user)
        else:
            print("Введены некоректные данные")
            # raise ValueError("Некорректные участники события")
    
    def participants_leavе(self, user):
        '''Выход участника из события.'''
        if user != self._organizer:
            self._participants.remove(user)
            print(f"Вы покинули событие {self._title}")
        else:
            print("Вы не можете покинуть событие так как являетесь его организатором")
            
    def change_description(self,user, new_description):
        '''Изменение описания события.'''
        if user == self._organizer and isinstance(user,User):
            self._description = new_description
            print(f"Описание события {self} изменено")
        else:
            print("Описание не может быть изменено")
    
    def del_description(self, user):
        '''Удаление описания события.'''
        if user == self._organizer and isinstance(user, User):
            self._description = None
        else:
            print("Описание не может быть удалено")
    
    def to_dict(self):
        event_dict = {
            'title': self._title,
            'organizer': self._organizer.to_dict(),
            'description': self._description,
            'participants': [{'name': participant.get_name(),'id': participant.get_id()} for participant in self._participants],
            'frequency': [dt.strftime("%Y-%m-%d") for dt in self._frequency]
        }
        return event_dict
    
    def write_to_json(self, filename='event_data.json'):
        event_dict = self.to_dict()
        event_json = json.dumps(event_dict, indent=2)
        with open(filename, 'w') as file:
            file.write(event_json)
    
    @classmethod
    def from_dict(cls, event_dict):
        title = event_dict.get('title')
        organizer_data = event_dict.get('organizer', {})
        organizer = User.from_dict(organizer_data)
        description = event_dict.get('description')
        participants_data = event_dict.get('participants', [])
        participants = {User.from_dict(participant) for participant in participants_data}
        frequency = [datetime.datetime.strptime(dt, "%Y-%m-%d").date() for dt in event_dict.get('frequency', [])]
        event = cls(title, organizer, description)
        event._participants = participants
        event._frequency = frequency
        return event
    
    @classmethod
    def read_from_json(cls, file='event_data.json'):
        with open(file, 'r') as f:
            event_dict = json.loads(f.read())
        return cls.from_dict(event_dict)
    
    @staticmethod
    def create_event_from_string(event_string):
        event_data = [item.strip() for item in event_string.split(',')]
        title = event_data[0]
        organizer_data = event_data[1].split(':')
        organizer_name = organizer_data[1].strip()
        date_str = event_data[2]
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return Event(title, organizer_name, date=date)
    



            
            
    
