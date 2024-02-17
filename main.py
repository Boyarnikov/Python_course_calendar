import flet as ft
from Routes import views_handler
from Start_page import Interface
# from Entrance import Interface
class Main(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 760
        page.window_height = 1000
        page.window_resizable = False
        page.window_maximizable = True
        appbar = Interface.navbar(page)
        page.add(appbar)
        page.update()
        def route_change(route):
            print(page.route)
            page.views.clear()
            page.views.append(
                views_handler(page)[page.route]
            )
        page.on_route_change = route_change
        page.go('/')

ft.app(target=Main)


        
        

    
    
   
    
    

    
    