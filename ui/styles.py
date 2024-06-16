import flet as ft

def apply_styles(page: ft.Page):
    # Création d'un objet ColorScheme avec les couleurs personnalisées
    custom_color_scheme = ft.ColorScheme(
        primary=ft.colors.BLUE,
        secondary=ft.colors.GREEN,
        background=ft.colors.WHITE,
        # Ajoutez d'autres couleurs si nécessaire
    )

    # Application du ColorScheme personnalisé au thème de la page
    #page.theme = ft.Theme(color_scheme=custom_color_scheme)
    
    # Application des autres styles de la page
    #page.padding = 20
    #page.spacing = 20
