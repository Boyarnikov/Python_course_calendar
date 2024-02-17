
import flet as ft
import time
def window(page: ft.Page):
    t = ft.Text(value="Hello World")
    page.controls.append(t)
    
    
    
    
    for i in range(1000):
        time.sleep(1)
        t.value = f"hello world {i}"
        page.update()

ft.app(target=window)