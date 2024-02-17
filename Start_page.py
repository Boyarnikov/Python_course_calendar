import flet as ft
import datetime

import sys
from Calendar import Calendar
from Backend import Backend
from User import User
from Event import Event
from Notification import NotificationManager

class Interface(ft.Container):
    """Описывает интерфейс входа в аккаунт"""
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

    def __init__(self,page: ft.Page):
        super().__init__()
        self.content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient([ft.colors.INDIGO_500, ft.colors.RED_200]),
            alignment=ft.alignment.Alignment(0, 0),
            content=
            ft.Container(
                ft.Stack([
                    ft.Container(
                        margin=ft.margin.only(top=300,bottom=700),
                        # alignment=ft.alignment.center,
                        # expand= True,
                        padding=ft.padding.all(20),
                        border_radius=11,
                        width=300,
                        height=300,
                        bgcolor='#33ffffff',
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=100,
                            color=ft.colors.BLUE_GREY_300,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        content=
                        ft.Column([
                            ft.Container(
                                content=(ft.Text("Calendar",color=ft.colors.BLUE_800,scale=2,size=10)),
                                width=300,
                                height=30,
                                alignment=ft.alignment.center
                                ),
                            ft.Container(
                                content=ft.ElevatedButton("Войти", on_click = self.show_entrance,
                                                          style = ft.ButtonStyle(
                                                          shape=ft.RoundedRectangleBorder(radius=10),),
                                                          bgcolor=ft.colors.BLUE_50,
                                                          ),
                                width=300,
                                height=50,
                                margin=ft.margin.only(top=30),

                                ),
                            ft.Container(
                                content=ft.ElevatedButton("Создать пользователя",color=ft.colors.BLACK,
                                                          on_click=self.show_create_new_user,
                                                          bgcolor=ft.colors.LIGHT_GREEN_ACCENT_200,
                                                          style=ft.ButtonStyle(
                                                          shape=ft.RoundedRectangleBorder(radius=10),
                                                          ),),
                                width=300,
                                height=50,
                                ),
                            ft.Container(
                                content=ft.TextButton("Забыли логин или пароль?",on_click= self.show_banner_click),
                                width=300,
                                height=50,
                                margin=ft.margin.only(top = 20,left=0),
                                opacity=1
                            ),
                        ],
                    ),
                    )

                ]),

                # alignment=ft.alignment.center,
                # expand=True
            ),

             )
        # self.alignment = ft.alignment.center
        # self.expand = True
        # Interface.navbar(None)
        
        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "Oops, К сожалению мы ничем не можем вам помоч. Вспоминайте свои данные или создавайте новый аккаунт."
            ),
            actions=[
                ft.TextButton("Вспомнить", on_click=self.close_banner),
                ft.TextButton("Не вспомнить", on_click=self.close_banner),

            ],
        )
    
    def show_banner_click(self,e):
        self.page.banner.open = True
        self.page.update()
    
    def close_banner(self,e):
        self.page.banner.open = False
        self.page.update()
    @staticmethod
    def navbar(page):
        navbar = ft.AppBar(
            leading=ft.Icon(ft.icons.CALENDAR_MONTH, color=ft.colors.BLUE_800),
            leading_width=100,
            title=ft.Text("КАЛЕНДАРЬ", color=ft.colors.BLUE_800),
            center_title=False,
            # bgcolor=ft.colors.LIME_100,
            toolbar_height=60,
            actions=[
                ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/')),
                
            ]
        )
        return navbar



    def show_create_new_user(self, e):
        username = ft.TextField(label="Введите имя пользователя: ", autofocus=True)
        password = ft.TextField(label="Придумайте пароль: ", autofocus=True)
        username_con = (ft.Container(
            content= username,
            width=300,
            height=50
        ))
        password_con = ft.Container(
            content=password,
            width=300,
            height=50
        )
        dlg_modal = ft.AlertDialog(
            modal=False,
            content=ft.Container(
                ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_color="blue700",
                            icon_size=20,
                            tooltip="Закрыть",
                            on_click=lambda x: x.page.close_dialog()),
                        ft.Container(
                            width=300,
                            height=200,
                            content=(
                                ft.Column(
                                    [
                                        ft.Container(content=username_con),
                                        ft.Container(content=password_con),
                                    ]
                                )
                            ),
                        )
                    ],
                    tight=True,
                ),
                padding=0,
            ),
            actions=[
                ft.ElevatedButton("Сохранить данные", on_click=lambda x: self.create_new_user(username,password,e))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda x: print("Modal dialog dismissed!"),
        )
        e.page.show_dialog(dlg_modal)


    def create_new_user(self,username,password,e):
        new_user = User(username.value, password.value)
        Interface.backend.add_users(new_user)
        Interface.backend.save_data_users()
        Interface.user = new_user
        show_user = ft.AlertDialog(
            title=ft.Text(f"Создан новый пользователь - {new_user} "), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        show_user.open = True
        self.page.update()
        e.page.show_dialog(show_user)

    def show_entrance(self,e):
        login = ft.TextField(label="Введите id пользователя: ", autofocus=True)
        password = ft.TextField(label="Введите пароль: ", autofocus=True,password = True)
        dlg_modal = ft.AlertDialog(
            modal=False,
            content=ft.Container(
                ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_color="blue700",
                            icon_size=20,
                            tooltip="Закрыть",
                            on_click=lambda x: x.page.close_dialog()),
                        ft.Container(
                            width=300,
                            height=200,
                            content=(
                                ft.Column(
                                    [
                                        ft.Container(content=login),
                                        ft.Container(content=password),
                                    ]
                                )
                            ),
                        )
                    ],
                    tight=True,
                ),
                padding=0,
            ),
            actions=[
                # ft.ElevatedButton("Войти", on_click=lambda x: self.entrance(login, password, e))
                ft.ElevatedButton("Войти", on_click = lambda x: self.entrance(login, password, e))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda x: print("Modal dialog dismissed!"),
        )
        e.page.show_dialog(dlg_modal)
        
    # def ent_close(self,login,password,e):
    #     self.entrance(login, password, e)
    #     e.page.close_dialog()


    def entrance(self,log,passw,e):
        login = log.value
        user_exists = False
        for user in Interface.backend.get_users():
            if user.get_id() == login:
                user_exists = True
                password = passw.value
                if user.check_password(password):
                    Interface.current_user = user
                    Interface.calendar = Calendar(user)
                    self.page.go("/main")
                    e.page.close_dialog()
                    e.page.close_banner()
                else:
                    show_user_password = ft.AlertDialog(
                        title=ft.Text("Пароль введен неверно"),
                        on_dismiss=lambda e: print("Dialog dismissed!")
                    )
                    "Диалоговое окно открывается при значении False. Причина не понятна  00))"
                    show_user_password.open = False
                    self.page.update()
                    e.page.show_dialog(show_user_password)
        if not user_exists:
            show_user = ft.AlertDialog(
                title=ft.Text("Пользователя не существует"),
                on_dismiss=lambda e: print("Dialog dismissed!")
            )
            show_user.open = True
            self.page.update()
            e.page.show_dialog(show_user)

class Notification_pr(ft.UserControl):
    """""Описывает интерфейс входа в аккаунт панели уведомлений"""
    def __init__(self,page):
        super().__init__()
        # self.page = page
        # self.notify = None
        
        self.notify_1 = ft.Row(
            scroll='always'
        )
        notifications = Notification_pr.view_notifications()
        for i in notifications:
            self.notify_1.controls.append(
                ft.Container(
                    padding=10,
                    width=175,
                    bgcolor='#55cc3333',
                    expand=False,
                    border_radius=30,
                    alignment=ft.alignment.top_center,
                    on_click=lambda e: print("Clickable without Ink clicked!"),
                    content=ft.Column(
                        horizontal_alignment=ft.alignment.top_center,
                        # alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=175,
                                height=20,
                                padding=ft.padding.only(right=130),
                                content=ft.Icon(name=ft.icons.CIRCLE_NOTIFICATIONS_OUTLINED,
                                                color=ft.colors.BLUE_800)
                            ),
                            ft.Text(i, size=15, color=ft.colors.BLUE_900),
                        
                        ]
                    )
                )
            )
    
    def build(self):
        self.notify = ft.Container(
            margin=ft.margin.only(top=0, left=10, right=10),
            height=150,
            # border_radius=10,
            visible=True,
            content=
            self.notify_1)
        return self.notify
    
    @staticmethod
    def view_notifications():
        notify = []
        notifications = Interface.notify.get_notifications()
        to_find = Interface.current_user
        if to_find is not None:
            user_to_find = to_find.get_id()
            found_notifications = False
            for notification in notifications:
                added_user = notification.get('AddedUser')
                if added_user == user_to_find:
                    found_notifications = True
                    organizer = notification.get('Organizer')
                    events = notification.get('Events')
                    notify.append(f"Пользователь {organizer} добавил вас в событие {events}.")
                remove_user = notification.get('RemoveUser')
                if remove_user == user_to_find:
                    found_notifications = True
                    organizer = notification.get('Organizer')
                    events = notification.get('Events')
                    notify.append(f"Пользователь {organizer} удалил вас из события {events}.")
            if not found_notifications:
                notify.append("Новых уведомлений нет")
        else:
            pass
        return reversed(notify)
    
    def add_control_to_page(self):
        control = Notification_pr(self)
        self.page.add(control)
    def set_visibility(self, visibility):
        """Метод для установки видимости контейнера."""
        if self.notify:
            self.notify.visible = visibility
            self.build().update()
         
class Event_tab(ft.UserControl):
    """Панель сздания нового события"""
    def __init__(self,page):
        super().__init__()
        # self.offset = ft.transform.Offset(-2, 0)
        # self.animate_offset = ft.animation.Animation(1000)
        self.name_event = ft.TextField(label="Название: ", autofocus=True)
        self.description_event = ft.TextField(
            label="Описание: ",
            multiline=True,
            min_lines=1,
            max_lines=3,
        )
        self.participants_event = ft.TextField(label="Участники: (через запятую)", on_change=self.search_now, on_submit=self.on_submit)
        self.periodic_event = ft.Dropdown(
            label="Периодичность",
            options=[
                ft.dropdown.Option("once"),
                ft.dropdown.Option("daily"),
                ft.dropdown.Option("weekly"),
                ft.dropdown.Option("monthly"),
                ft.dropdown.Option("yearly")
            ],
            width=200,
            )
        
        self.gg = ft.Dropdown(
                label="ГГ",
                dense=True,
                options=[ft.dropdown.Option(i) for i in range(2024, 2050)],
                width=100)
        
        self.mm = ft.Dropdown(
                label="MM",
                dense=True,
                options=[ft.dropdown.Option(i) for i in range(1, 13)],
                width=100)
        self.dd = ft.Dropdown(
                label="ДД",
                dense=True,
                options=[ft.dropdown.Option(i) for i in range(1, 32)],
                width=100)
        
        self.date_input = ft.Row([
            self.gg,
            self.mm,
            self.dd
        ])
        
        self.data = Interface.backend.get_users()
        self.resultdata = ft.ListView()
        self.resultcon = ft.Container(
            bgcolor="red200",
            padding=10,
            margin=10,
            offset=ft.transform.Offset(-2, 0),
            animate_offset=ft.animation.Animation(600, curve="easeIn"),
            content=ft.Column([self.resultdata])
        )
    
    def search_now(self, e):
        mysearch = e.control.value
        self.resultdata.controls.clear()
        if mysearch:
            search_t = [term.strip() for term in mysearch.split(",")]
            for user in self.data:
                for term in search_t:
                    if term and term in str(user):
                        self.resultdata.controls.append(
                            ft.Text(str(user), size=20, color="white")
                        )
            self.resultcon.visible = bool(self.resultdata.controls)
            if self.resultcon.visible:
                self.resultcon.offset = ft.transform.Offset(0, 0)
            else:
                self.resultcon.offset = ft.transform.Offset(-2, 0)
        else:
            self.resultcon.visible = False
        self.page.update()
    def on_submit(self,e):
        self.search_now(e)
        
    def build(self):
        save_event = ft.ElevatedButton("Сохранить",
                                       color="white",
                                       bgcolor='#443366ff',
                                       on_click=lambda _: self.create_event(self.name_event,
                                                                                 self.description_event,
                                                                                 self.participants_event,
                                                                                 self.periodic_event)
                                   
                                       )
        
        
        con_create_event = ft.Container(
            width=500,
            # height=500,
            # margin=ft.margin.all(20),
            padding=ft.padding.only(left=10,right=10,bottom=10),
            bgcolor='#443366ff',
            # visible=True,
            expand=True,
            alignment=ft.alignment.center,
            border_radius=20,
            # offset=ft.transform.Offset(-2, 0),
            # animate_offset=ft.animation.Animation(1000),
            # offset=self.offset,
            # animate_offset=self.animate_offset,
            content=ft.Column(
                expand=True,
                controls=[
                        ft.Container(
                            height=50,
                            width=1000,
                            bgcolor=ft.colors.LIGHT_BLUE_900,
                            margin=ft.margin.only(left=-10,right=-10),
                            content=ft.Container(
                                bgcolor=ft.colors.LIGHT_BLUE_900,
                                alignment=ft.alignment.center,
                                content=ft.Text("Создать событие", color="white", size=15)
                            ),
                        ),
                        ft.Column([
                                self.name_event,
                                self.description_event,
                                self.participants_event,
                                self.date_input,
                                
                                self.periodic_event,
                                save_event
                                
                            ])
                      

                    ])
            )
        return con_create_event
    
    
 
    def create_event(self,title,description, participant_ev, periodic):
        organizer = Interface.current_user
        new_event = Event(title.value, organizer, description.value)
        Interface.event = new_event
        Interface.backend.add_events(new_event)
        print("Участники доступные для добавления в событие: ", Interface.backend.get_users())
        participants_str = participant_ev.value
        participants_names = [name.strip() for name in participants_str.split(',')]
        added_participants = []
        for participant_name in participants_names:
            participant = next((user for user in Interface.backend.get_users() if user.get_id() == participant_name),
                               None)
            if participant:
                new_event.add_part(organizer, participant)
                added_participants.append(participant)
            else:
                print(f"Пользователь {participant_name} не найден.")
        start_date = f"{self.gg.value}-{self.mm.value}-{self.dd.value}"
        frequency = periodic.value
        new_event.create_periodic_event(start_date, frequency)
        print(f"Событие {new_event.get_title} создано.")
        Interface.backend.save_data_events()
        for participant in added_participants:
            remove_user = None
            Interface.notify.notify_added_to_event(organizer, participant, remove_user, new_event)
        Interface.notify.save_notifications()
        self.dia_ev(self)
        
    def dia_ev(self,e):
        show_user = ft.AlertDialog(
            title=ft.Text(f"Созданo новое событие"), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        show_user.open = True
        self.name_event.value = ""
        self.periodic_event.value = ""
        self.participants_event.value = ""
        self.description_event.value = ""
        self.page.update()
        e.page.show_dialog(show_user)
        
class Main_page(ft.Row):
    """Главная страница приложения"""
    def __init__(self,page: ft.Page,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.page = page
        self.notification = Notification_pr(self)
        self.event_tab = Event_tab(self,)
        self.content_1 = (ft.Container(
            height=1500,
            expand=True,
            alignment=ft.alignment.center_left,
            content=
            ft.Row(
                [
                    ft.Container(
                        # bgcolor=ft.colors.LIME_100,
                        content=
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Divider(height=1, color=ft.colors.BLUE_GREY_300),
                                ft.TextButton(
                                    on_click=self.animate_container_event,
                                    width=200,
                                    height=40,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=1), ),
                                    content=ft.Row([
                                        ft.Icon(name=ft.icons.CREATE, color=ft.colors.BLUE_800),
                                        ft.Text("Создать")],
                                    )
                                ),
                                ft.TextButton(
                                    on_click=self.animate_container_show_all_event,
                                    width=200,
                                    height=40,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=1)),
                                    content=ft.Row([
                                        ft.Icon(name=ft.icons.EMOJI_EVENTS_OUTLINED, color=ft.colors.BLUE_800),
                                        ft.Text("Все события")],
                                    )
                                ),
                                ft.TextButton(
                                    on_click=self.animate_container_show_calendar,
                                    width=200,
                                    height=40,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=1), ),
                                    content=ft.Row([
                                        ft.Icon(name=ft.icons.CALENDAR_VIEW_MONTH_ROUNDED, color=ft.colors.BLUE_800),
                                        ft.Text("Календарь")],
                                    )
                                ),
                                ft.TextButton(
                                    on_click=self.animate_notification,
                                    width=200,
                                    height=40,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=1), ),
                                    content=ft.Row([
                                        ft.Icon(name=ft.icons.NOTIFICATIONS, color=ft.colors.BLUE_800),
                                        ft.Text("Уведомления")],
                                    
                                    )
                                ),
                                ft.TextButton(
                                    width=200,
                                    height=40,
                                    on_click=lambda _: self.page.go('/'),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=1), ),
                                    content=ft.Row([
                                        ft.Icon(name=ft.icons.EXIT_TO_APP, color=ft.colors.BLUE_800),
                                        ft.Text("Выход")],
                                    )
                                ), ]
                        ),
                        width=200,
                        expand=False,
                    ),
                    ft.VerticalDivider(width=1, color=ft.colors.BLUE_GREY_300),
                    ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        # bgcolor=ft.colors.LIGHT_BLUE_200,
                        bgcolor=ft.colors.WHITE10,
                        content=
                        ft.Column([
                            ft.Divider(height=1, color=ft.colors.BLUE_GREY_300),
                            # self.notify,
                            self.notification,
                            ft.Container(
                                margin=ft.margin.only(left=10, right=10),
                                height=450,
                                # width=100,
                                expand=False,
                                # bgcolor=ft.colors.RED_200,
                                border_radius=20,
                                content=
                                ft.Row(
                                    scroll="alwais",
                                    controls=[
                                        self.event_tab,
                                        self.show_all_event,
                                        self.show_calendar
                                    ]
                                )
                            ),
                        ]),
                    )
                ],
                spacing=0,
                expand=True,
            )
        ))

        self.controls = [
            self.content_1
        ]
 
 
    show_all_event = ft.Container(
        width=500,
        height=500,
        # bgcolor='#443366ff',
        bgcolor='green',
        expand=True,
        # visible=True,
        offset=ft.transform.Offset(-3, 0),
        animate_offset=ft.animation.Animation(1000),
        alignment=ft.alignment.center,
        border_radius=10
    )

    show_calendar = ft.Container(
        width=500,
        height=500,
        # bgcolor='#443366ff',
        bgcolor='red',
        expand=True,
        # visible= True,
        offset=ft.transform.Offset(-4, 0),
        animate_offset=ft.animation.Animation(1000),
        alignment=ft.alignment.center,
        border_radius=10
    )
    
    
    # def animate_container_event(self,e):
    #     if self.event_tab.offset == ft.transform.Offset(0, 0):
    #         self.event_tab.offset = ft.transform.Offset(-2, 0)
    #     elif self.event_tab.offset == ft.transform.Offset(-2, 0):
    #         self.event_tab.offset = ft.transform.Offset(0, 0)
    #     self.event_tab.update()
    def animate_container_event(self, e):
        self.event_tab.visible = not self.event_tab.visible
        self.page.update()
    
    def animate_container_show_all_event(self, e):
        if self.show_all_event.offset == ft.transform.Offset(0, 0):
            self.show_all_event.offset = ft.transform.Offset(-3, 0)
        elif self.show_all_event.offset == ft.transform.Offset(-3, 0):
            self.show_all_event.offset = ft.transform.Offset(0, 0)
        self.show_all_event.update()
    
    
    def animate_container_show_calendar(self, e):
        if self.show_calendar.offset == ft.transform.Offset(0, 0):
            self.show_calendar.offset = ft.transform.Offset(-4, 0)
        elif self.show_calendar.offset == ft.transform.Offset(-4, 0):
            self.show_calendar.offset = ft.transform.Offset(0, 0)
        self.show_calendar.update()
    
    
    def animate_notification(self, e):
        self.notification.visible = not self.notification.visible
        self.page.update()

    