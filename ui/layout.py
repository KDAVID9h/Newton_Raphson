import flet as ft
from ui.widgets import UIWidgets, init_ui
from .styles import apply_styles

async def create_layout(page: ft.Page):
    init_ui(page)
    apply_styles(page)

        #ui_widgets = UIWidgets(page)
    #input_fields = ui_widgets.create_input_fields()
    #buttons = ui_widgets.create_buttons()
    #output_area = ui_widgets.create_output_area()

    #page.add(ft.Column(
        #controls=[
            #input_fields,
            #buttons,
            #output_area,
        #],
        #scroll=ft.ScrollMode.AUTO
    #))
