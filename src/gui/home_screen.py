import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from util.smart_tv_app_logic import SmartTVAppLogic
import util.util_imagenes as util_img

class HomeScreen():

    def __init__(self, panel_principal, app_logic):
        
        button_width = 200
        button_height = 200
        button_font = font.Font(family='FontAwesome', size=15)

        self.buttonNetflix = tk.Button( panel_principal )
        self.nextflixImg = util_img.leer_imagen("./../src/img/Netflix.png", (200, 200))
        self.buttonGoogle = tk.Button( panel_principal )
        self.googleImg = util_img.leer_imagen("./../src/img/Google.png", (200, 200))

        buttons_info = [
            ("Netflix", self.nextflixImg, self.buttonNetflix, app_logic.open_netflix_kiosk)
            ("Google", self.googleImg, self.buttonGoogle, app_logic.open_google_kiosk)
        ]

        for text, img, button, command in buttons_info:
            self.buttons_config(text, img, button, button_font, button_width, button_height, command)

    def buttons_config(self, text, img, button, button_font, button_width, button_height, command):
        button.config(text=f"{text}", image=img, anchor="center", font=button_font,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=button_width, height=button_height,
                      highlightthickness = 0,
                      command = command)
        button.pack(side=tk.LEFT, expand=True)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')