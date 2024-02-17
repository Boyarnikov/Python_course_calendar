"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""
import datetime
import sys
from Calendar import Calendar
from Backend import Backend
from User import User
from Event import Event
from Notification import NotificationManager
class Interface():
    user = None
    event = None
    calendar = None
    current_user = None
    state = "start"
    backend = Backend()
    notify = NotificationManager()
    backend.load_data_users()
    backend.load_data_events()
    backend.load_data_calendar()
    notify.load_notifications()
    @staticmethod
    def start():
        ret = input("""Начало работы
        0)Войти в аккаунт
        1)Создать нового пользователя
        2)Завершить работу
        """)
        if ret == "0":
            Interface.entrance()
        elif ret == "1":
            Interface.create_new_user()
        elif ret == "2":
            Interface.finish()
            
    @staticmethod
    def main_menu():
        i = input("""Главное меню
        0)Завершить работу
        1)Создать событие
        2)Добавить в событие пользователей
        3)Удалить пользователей из события
        4)Удалить событие
        5)Просмотреть все свои события
        6)Покинуть событие
        7)Изменить описание события
        8)Просмотреть события в промежутке дат
        9)Просмотр Календаря
        10)Просмотреть уведомления
        11)Выйти из аккаунта
        """)
        if i == "0":
            Interface.finish()
        elif i == "1":
            Interface.create_event()
        elif i == "2":
            Interface.add_user_in_event()
        elif i == "3":
            Interface.remove_users_from_events()
        elif i == "4":
            Interface.del_events()
        elif i == "5":
            print(Interface.backend.view_the_events_user(Interface.current_user))
            Interface.main_menu()
        elif i == "6":
            Interface.leave_event()
        elif i == "7":
            Interface.change_description()
        elif i == "8":
            Interface.search_event()
        elif i == "9":
            Interface.view_the_calendar()
            Interface.main_menu()
        elif i == "10":
            Interface.notifications()
        elif i == "11":
            Interface.start()
 
    @staticmethod
    def notifications():
        i = input("""Уведомления
        0)Просмотреть все уведомления
        1)Пометить уведомления как прочитанные
        2)Главное меню
        """)
        if i == "0":
            Interface.view_notifications()
            Interface.notifications()
        if i == "1":
            Interface.mark_notifications_as_read()
            Interface.notify.save_notifications()
            Interface.notifications()
        if i == "2":
            Interface.main_menu()
    
    @staticmethod
    def entrance():
        login = input("Введите свой логин(id): ")
        user = Interface.backend.entrance(login)
        if user:
            Interface.current_user = user
            Interface.calendar = Calendar(user)
            Interface.main_menu()
        else:
            Interface.start()
            
    @staticmethod
    def create_event():
        title = input("Введите название события: ")
        organizer = Interface.current_user
        description = input("Введите описание события (или оставьте пустым): ")
        new_event = Event(title, organizer, description)
        Interface.event = new_event
        Interface.backend.add_events(new_event)
        print("Участники доступные для добавления в событие: ", Interface.backend.get_users())
        participants_str = input("Введите id участников (разделяйте запятыми): ")
        participants_names = [name.strip() for name in participants_str.split(',')]
        added_participants = []
        for participant_name in participants_names:
            participant = next((user for user in Interface.backend.get_users() if user.get_id() == participant_name), None)
            if participant:
                new_event.add_part(organizer, participant)
                added_participants.append(participant)
            else:
                print(f"Пользователь {participant_name} не найден.")
        start_date = input("Введите дату начала события (гггг-мм-дд): ")
        frequency = input("Введите частоту события (once, daily, weekly, monthly, yearly): ")
        new_event.create_periodic_event(start_date, frequency)
        print(f"Событие {new_event.get_title} создано.")
        print("Список всех ваших событий: ", Interface.backend.get_events_user(Interface.current_user))
        for participant in added_participants:
            remove_user = None
            Interface.notify.notify_added_to_event(organizer, participant, remove_user, new_event)
        Interface.notify.save_notifications()
        Interface.main_menu()
  
    @staticmethod
    def get_calendar():
        calendars = []
        for cal in Interface.backend.get_calendars():
            if Interface.current_user == cal.get_organizer_cal():
                calendars.append(cal)
        return calendars
    
    @staticmethod
    def add_user_in_event():
        admin = Interface.current_user
        name_events = [event.get_title() for event in Interface.backend.get_events_user(admin)]
        print("Введите название события из списка для добавления в него участников ", name_events)
        event_title = input()
        selected_event = next((event for event in Interface.backend.get_events_user(admin) if event.get_title() == event_title), None)
        
        if selected_event:
            print("Участники доступные для добавления в событие: ", Interface.backend.get_users())
            participants_str = input("Введите id участников (разделяйте запятыми): ")
            participant_names = [name.strip() for name in participants_str.split(',')]
            
            added_participants = []
            for participant_name in participant_names:
                participant = next((user for user in Interface.backend.get_users() if user.get_id() == participant_name), None)
                
                if participant:
                    if participant in selected_event.get_participants():
                        print(f"Участник {participant.get_name()} уже присутствует в событии {event_title}. Пропущен.")
                    else:
                        selected_event.add_part(admin, participant)
                        print(f"Участник {participant.get_name()} добавлен в событие {event_title}.")
                        added_participants.append(participant)
                else:
                    print(f"Пользователь {participant_name} не найден.")
            
            if added_participants:
                remove_user = None
                for participant in added_participants:
                    Interface.notify.notify_added_to_event(admin, participant,remove_user, selected_event)
                Interface.notify.save_notifications()
            
            Interface.main_menu()
        else:
            print(f"Событие с названием {event_title} не найдено.")
            Interface.main_menu()
    
    @staticmethod
    def remove_users_from_events():
        admin = Interface.current_user
        name_events = [event.get_title() for event in Interface.backend.get_events_user_org(admin)]
        print("Введите название события из списка для удаления из него участников ", name_events)
        event_title = input()
       
        selected_event = Interface.backend.selected_event(admin,event_title)
        if selected_event:
            print("Участники доступные для удаления из события: ", selected_event.get_participants())
            participants_str = input("Введите id участников (разделяйте запятыми): ")
            participant_names = [name.strip() for name in participants_str.split(',')]
            remove_participants = []
            for participant_name in participant_names:
                participant = next((user for user in Interface.backend.get_users() if user.get_id() == participant_name), None)
                if participant:
                    if participant not in selected_event.get_participants():
                        print(f"Участник {participant.get_name()} отсутствует в событии {event_title}. Пропущен.")
                    else:
                        selected_event.del_participants(event_title, admin, participant)
                        print(f"Участник {participant.get_name()} Удален из события {event_title}.")
                        remove_participants.append(participant)
                else:
                    print(f"Пользователь {participant_name} не найден.")
                    Interface.main_menu()
            if remove_participants:
                added_user = None
                for participant in remove_participants:
                    Interface.notify.notify_remove_from_event(admin,added_user, participant, selected_event)
                Interface.notify.save_notifications()
                Interface.main_menu()
        else:
            print(f"Событие с названием {event_title} не найдено.")
            Interface.main_menu()
        
    @staticmethod
    def create_new_user():
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        new_user = User(username, password)
        Interface.backend.add_users(new_user)
        Interface.backend.save_data_users()
        Interface.user = new_user
        print(f"Создан новый пользователь: {new_user}")
        i = input("""
        0)Завершить работу
        1)Войти в созданный аккаунт
        """)
        if i == "0":
            Interface.finish()
        elif i == "1":
            Interface.entrance()
    @staticmethod
    def view_notifications():
        notifications = Interface.notify.get_notifications()
        user_to_find = Interface.current_user.get_id()
        found_notifications = False
        for notification in notifications:
            added_user = notification.get('AddedUser')
            if added_user == user_to_find:
                found_notifications = True
                organizer = notification.get('Organizer')
                events = notification.get('Events')
                print(f"Пользователь {organizer} добавил вас в событие {events}.")
            remove_user = notification.get('RemoveUser')
            if remove_user == user_to_find:
                found_notifications = True
                organizer = notification.get('Organizer')
                events = notification.get('Events')
                print(f"Пользователь {organizer} удалил вас из события {events}.")
        if not found_notifications:
            print("Новых уведомлений не найдено.")
            
    @staticmethod
    def mark_notifications_as_read():
        user_to_find = Interface.current_user.get_id()
        Interface.notify.remove_notifications(user_to_find)
        print("Уведомления удалены")

    @staticmethod
    def view_the_calendar():
        Interface.backend.viewing_calendar(Interface.current_user, Interface.calendar)
        Interface.calendar.clear_calendar()
        Interface.main_menu()
    @staticmethod
    def search_event():
        start_date = input("Введите начальную дату: ")
        end_date = input("Введите конечную дату: ")
        for i in Interface.backend.get_events_user(Interface.current_user):
            Interface.calendar.add_event_cal(i)
        Interface.calendar.sort_events()
        Interface.calendar.search_event(start_date, end_date)
        Interface.calendar.clear_calendar()
        Interface.main_menu()
    @staticmethod
    def del_events():
        user = Interface.current_user
        print(Interface.backend.get_events_title_user_org(user))
        event = input("Введите название события из списка: ",)
        Interface.backend.remove_events(event)
        Interface.main_menu()
    
    @staticmethod
    def leave_event():
        user = Interface.current_user
        print(Interface.backend.get_events_title_user(user))
        event_name = input("Введите событие из списка которое вы хотите покинуть: ")
        selected_event = Interface.backend.selected_event(user,event_name)
        if selected_event:
            selected_event.participants_leavе(user)
            Interface.main_menu()
        else:
            print(f"Событие {selected_event} не найдено.")
            Interface.main_menu()
    @staticmethod
    def change_description():
        user = Interface.current_user
        print(Interface.backend.get_events_title_user(user))
        event_name = input("Введите событие из списка описание которого вы хотите изменить: ")
        selected_event = Interface.backend.selected_event(Interface.current_user, event_name)
        desc = input("Введите новое описание события")
        selected_event.change_description(Interface.current_user,desc)
        
        Interface.main_menu()
        
    @staticmethod
    def finish():
        print("Работа программы завершена.")
        Interface.backend.save_data_events()
        sys.exit(0)

Interface.start()



