import flet as ft
#import asyncio
from ui.layout import create_layout

async def main(page: ft.Page):
    page.adaptive = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Résolution des Systèmes d'Équations Non Linéaires"
    page.scroll = 'HIDDEN'
    page.theme_mode = ft.ThemeMode.SYSTEM

    # Construisez l'écran principal
    await create_layout(page)
    
    # Mettez à jour la page pour afficher l'écran principal
    page.update()

ft.app(target=main, assets_dir="assets")

    #page.bgcolor = "background-color: #RRGGBB;"
    
    # Créez un objet VideoMedia pour votre vidéo
    #video_media = ft.VideoMedia("assets/splash.mp4")  # Assurez-vous que le chemin est correct
    
    # Ajoutez le widget vidéo pour l'écran de démarrage
    #splash_video = ft.Video(
    #    playlist=[video_media],  # Utilisez la liste de lecture avec votre VideoMedia
    #    autoplay=True,
        #controls=False,  # Mettez à True si vous voulez afficher les contrôles de la vidéo
        #loop=True  # Mettez à False si vous ne voulez pas que la vidéo se répète
    #)
    #page.add(splash_video)
    
    # Mettez à jour la page pour afficher l'écran de démarrage
    #page.update()
    
    # Attendez quelques secondes de manière asynchrone
    #await asyncio.sleep(6)
    
    # Retirez l'écran de démarrage
    #page.remove(splash_video)
