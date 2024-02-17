import flet as ft
from Start_page import Main_page,Interface

def views_handler(page):
  return {
    '/':ft.View(
        route='/',
        controls=[
          Interface(page)
        ]
      ),
    '/main':ft.View(
        route='/main',
        controls=[
          Main_page(page)
        ]
      ),
  }