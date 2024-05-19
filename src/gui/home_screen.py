import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from util.smart_tv_app_logic import SmartTVAppLogic
import util.util_imagenes as util_img

class HomeScreen():

    def __init__(self, panel_principal, app_logic):
        
        self.button_width = 250
        self.button_height = 250
        self.button_font = font.Font(family='FontAwesome', size=15)

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame( panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame( panel_principal)
        self.barra_inferior.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        self.superior_row = tk.Frame( self.barra_inferior )
        self.superior_row.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.superior_row.pack(side=tk.TOP, fill='both', expand=True)  
        self.inferior_row = tk.Frame( self.barra_inferior )
        self.inferior_row.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.inferior_row.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_superior, text="MaFE TV")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        self.buttonNetflix = tk.Button( self.superior_row )
        self.nextflixImg = util_img.leer_imagen("./../src/img/Netflix.png", (self.button_width, self.button_height))
        self.buttonGoogle = tk.Button( self.superior_row )
        self.googleImg = util_img.leer_imagen("./../src/img/Google.png", (self.button_width, self.button_height))
        self.buttonYoutube = tk.Button( self.superior_row )
        self.youtubeImg = util_img.leer_imagen("./../src/img/Youtube.png", (self.button_width, self.button_height))
        self.buttonSpotify = tk.Button( self.inferior_row )
        self.spotifyImg = util_img.leer_imagen("./../src/img/Spotify.png", (self.button_width, self.button_height))
        self.buttonHBO = tk.Button( self.inferior_row )
        self.HBOImg = util_img.leer_imagen("./../src/img/HBO.png", (self.button_width, self.button_height))
        self.buttonF1 = tk.Button( self.inferior_row )
        self.F1Img = util_img.leer_imagen("./../src/img/F1.png", (self.button_width, self.button_height))

        buttons_info = [
            ("Netflix", self.nextflixImg, self.buttonNetflix, app_logic.open_netflix_kiosk),
            ("Google", self.googleImg, self.buttonGoogle, app_logic.open_google_kiosk),
            ("Youtube", self.youtubeImg, self.buttonYoutube, app_logic.open_youtube_kiosk),
            ("Spotify", self.spotifyImg, self.buttonSpotify, app_logic.open_spotify_kiosk),
            ("HBO", self.HBOImg, self.buttonHBO, app_logic.open_hbo_kiosk),
            ("F1TV", self.F1Img, self.buttonF1, app_logic.open_f1_kiosk),
        ]

        for text, img, button, command in buttons_info:
            self.buttons_config(text, img, button, self.button_font, self.button_width, self.button_height, command)

    def buttons_config(self, text, img, button, button_font, button_width, button_height, command):
        button.config(text=f"{text}", image=img, anchor="center", font=button_font,
                      bd=0, bg=COLOR_CUERPO_PRINCIPAL, fg="white", width=button_width, height=button_height,
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
        button.config(width=self.button_width + 20, height=self.button_height + 20, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(width=self.button_width, height=self.button_height, fg='white')