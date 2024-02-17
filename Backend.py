"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.
"""
import ast
from datetime import datetime
from Event import Event
from User import User
from Calendar import Calendar
from Notification import NotificationManager
import csv

class Backend:
    _instance = None
    file_users = 'backend_data_users.csv'
    file_events = 'backend_data_events.csv'
    file_calendar = 'backend_data_calendar.csv'
  
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Backend, cls).__new__(cls, *args, **kwargs)
            cls._instance._users = []
            cls._instance._events = []
            cls._instance._back_calendar = list()
            cls._instance._list_notify = list()
        return cls._instance
    
    def __repr__(self):
        return f"Users:{self._users}"
    
    def __str__(self):
        return f"Users:{self._users},{self._back_calendar}"
   
    def get_list_notify(self):
        return self._instance._list_notify
    def get_events_title_user(self, user):
        'Метод выдает название событий пользователя в которых он участвует'
        name_events = [event.get_title() for event in self.get_events_user(user)]
        return name_events
    
    def get_events_title_user_org(self, user):
        'Метод выдает название событий пользователя которые он создал'
        name_events = [event.get_title() for event in self.get_events_user_org(user)]
        return name_events
    def add_users(self, user):
        self._instance._users.append(user)
    
    def get_users(self):
        return self._users
    
    def get_events(self):
        return self._events
    def add_events(self, event):
        return self._instance._events.append(event)
    def get_calendars(self):
        return self._back_calendar
    def add_calendar(self, calendar):
        if isinstance(calendar, Calendar):
            self._instance._back_calendar.append(calendar)
        else:
            print("Ошибка: Попытка добавить неэкземпляр Calendar.")
    
    def save_data_users(self):
        with open(self.file_users, mode='w', newline='') as file:
            fieldnames = ['Login', 'Password', 'Id']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self._users:
                writer.writerow({'Login': user.get_name(), 'Password': user.get_password(), 'Id': user.get_id()})

    def save_data_events(self):
        with open(self.file_events, mode='w', newline='') as file:
            fieldnames = ['title', 'organizer', 'description', 'participants', 'frequency']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for event in self._events:
                writer.writerow({
                    'title': event.get_title(),
                    'organizer': event.get_organizer().get_name(),
                    'description': event.get_description() if True else None,
                    'participants': ', '.join(user.get_name() for user in event.get_participants()),
                    'frequency': ', '.join(date.strftime("%Y-%m-%d") for date in event.get_frequency_event())
                })
    def save_data_calendar(self):
            with open(self.file_calendar, 'w', newline='') as file:
                fieldnames = ['organizer_cal', 'date', 'events']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for calendar in self._back_calendar:
                    organizer, events = calendar.get_calendar()
                    for date, events_list in events.items():
                        formatted_date = date.strftime("%Y-%m-%d")

                        events_data = []
                        for event in events_list:
                            events_data.append({
                                'title': event.get_title(),
                                'organizer': event.get_organizer().get_name(),
                                'description': event.get_description() if True else None,
                                'participants': ', '.join(user.get_name() for user in event.get_participants()),
                                'frequency': ', '.join(date.strftime("%Y-%m-%d") for date in event.get_frequency_event())
                            })
                        writer.writerow({'organizer_cal': organizer.get_name(),
                                         'date': formatted_date,
                                         'events': events_data})

    def load_data_users(self):
        try:
            with open(self.file_users, mode='r') as file:
                reader = csv.DictReader(file)
                self._users = []
                for row in reader:
                    login = row['Login']
                    password_hash = row['Password']
                    user_id = row['Id']
                    user = User(login, password_hash, user_id)
                    self._users.append(user)
        except FileNotFoundError:
            pass
    
    def load_data_events(self):
        try:
            with open(self.file_events, mode='r') as file:
                reader = csv.DictReader(file)
                self._events = []
                for row in reader:
                    title = row['title']
                    organizer_name = row['organizer']
                    description = row['description']
                    organizer = next((user for user in self._users if user.get_name() == organizer_name), None)
                    if organizer:
                        event = Event(title, organizer, description)
                        participants = row['participants'].split(', ')
                        for participant_name in participants:
                            participant = next((user for user in self._users if user.get_name() == participant_name),None)
                            if participant:
                                event.add_part(organizer, participant)
                        frequencies = row['frequency'].split(', ')
                        for date_str in frequencies:
                            date = datetime.strptime(date_str, "%Y-%m-%d").date()
                            event.create_periodic_event(date, "once")
                        self._events.append(event)
        except FileNotFoundError:
            pass
    
    def load_data_calendar(self):
        try:
            with open(self.file_calendar, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    organizer_cal, date_str, events_data_str = row
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    organizer_c = next((user for user in self._users if user.get_name() == organizer_cal), None)
                    if organizer_c:
                        events_data = ast.literal_eval(events_data_str)
                        for ev in events_data:
                            title = ev.get('title')
                            organizer_event = ev.get('organizer')
                            description = ev.get('description')
                            organizer_e = next((user for user in self._users if user.get_name() == organizer_event),None)
                            if not (title and organizer_e):
                                print(f"Пропущена строка: {row}. Неполные данные о событие.")
                                continue
                            event = Event(title, organizer_e, description)
                            participants = ev.get('participants', '').split(', ')
                            for participant_name in participants:
                                participant = next((user for user in self._users if user.get_name() == participant_name), None)
                                if participant:
                                    event.add_part(organizer_e, participant)
                            frequencies = ev.get('frequency', '').split(', ')
                            for date_str in frequencies:
                                date_ev = datetime.strptime(date_str, "%Y-%m-%d").date()
                                event.create_periodic_event(date_ev, "once")
                            calendar = Calendar(organizer_c)
                            calendar.add_event_cal(event)
                            self._back_calendar.append(calendar)
        except FileNotFoundError:
            print(f"Error: Файл не найден - {self.file_calendar}")
        except Exception as e:
            print(f"Error: {e}")
  
    def entrance(self, login):
        user_exists = False
        for user in self.get_users():
            if user.get_id() == login:
                user_exists = True
                password = input("Введите пароль: ")
                print(f"Введенный пароль: {password}")
                print(f"Сохраненный хэш пароля: {user.get_password()}")
                if user.check_password(password):
                    print("Добро пожаловать, ", user)
                    return user
                else:
                    print("Пароль введен неверно, выполните вход заново")
                    return None
        if not user_exists:
            print("Пользователя не существует, выполните вход заново")
            return None
        
    def viewing_calendar(self, user, calendar):
        'Метод выдает календарь пользователя'
        for i in self.get_events_user(user):
            calendar.add_event_cal(i)
        calendar_data = calendar.get_calendar()
        for date, events_list in calendar_data.items():
            print(f"Дата: {date.strftime('%Y-%m-%d')}")
            for event in events_list:
                print(f" {event.get_title()}")
                print(f"Описание: {event.get_description()}")
                participants = ', '.join(user.get_name() for user in event.get_participants())
                print(f"Участники: {participants}")
                print("-------------------------------")
    
    def get_events_user(self, user):
        'Метод выдает список всех событий пользователя'
        events = []
        for event in self.get_events():
            if user in event.get_participants():
                events.append(event)
        return events
    
    def get_events_user_org(self, user):
        'Метод выдает список событий пользователя которые он создал'
        events = []
        for event in self.get_events():
            if user == event.get_organizer():
                events.append(event)
        return events
    
    def remove_events(self,event_title):
        events = self.get_events()
        event_to_remove = next((event for event in events if event.get_title() == event_title), None)
        if event_to_remove:
            events.remove(event_to_remove)
            print(f"Событие {event_title} удалено.")
        else:
            print(f"Событие {event_title} не найдено.")
    
    def selected_event(self,admin, event_title):
        'Метод ищет событие по имени в списке событий пользователя'
        selected_event = next((event for event in self.get_events_user(admin) if event.get_title() == event_title), None)
        return selected_event
    
    def selected_event_org(self,admin, event_title):
        'Метод ищет событие по имени в списке событий пользователя'
        selected_event = next((event for event in self.get_events_user_org(admin) if event.get_title() == event_title), None)
        return selected_event
    
    def view_the_events_user(self,user):
        events = self.get_events_user(user)
        for event in events:
            print(f"Название: {event.get_title()}")
            print(f"Описание: {event.get_description()}")
            participants = ', '.join(user.get_name() for user in event.get_participants())
            print(f"Участники: {participants}")
            frequencies = ', '.join(date.strftime("%Y-%m-%d") for date in event.get_frequency_event())
            print(f"Даты проведения: {frequencies}")
            print()
    
        