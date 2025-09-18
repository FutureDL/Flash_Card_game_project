import flet as ft
import scripts.FlashCardApp as MainPage


def main(page: ft.Page):
    page.title = "FlashCardApp"
    page.window.width = 1100
    page.window.height = 780
    page.window.center()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    
    page.add(MainPage.MainPage(page))
    
ft.app(target=main)