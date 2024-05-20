import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from util.smart_tv_app_logic import SmartTVAppLogic
import util.util_imagenes as util_img

from gui.video_options_screen import VideoScreen
from gui.images_screen import ImagesScreen
from gui.music_screen import MusicScreen

class MixtoScreen():

    def __init__(self, panel_principal, app_logic):
        
        self.cuerpo_principal = panel_principal
        self.app_logic = app_logic

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
            self.barra_superior, text="Elije una accion")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        self.buttonVideo = tk.Button( self.superior_row )
        self.videoImg = util_img.leer_imagen("./../src/img/Video.png", (self.button_width, self.button_height))
        self.buttonImagen = tk.Button( self.superior_row )
        self.imagenImg = util_img.leer_imagen("./../src/img/Imagen.png", (self.button_width, self.button_height))
        self.buttonMusica = tk.Button( self.superior_row )
        self.musicaImg = util_img.leer_imagen("./../src/img/Musica.png", (self.button_width, self.button_height))

        buttons_info = [
            ("Video", self.videoImg, self.buttonVideo, self.abrir_video_options_screen),
            ("Imagen", self.imagenImg, self.buttonImagen, self.abrir_images_screen),
            ("Música", self.musicaImg, self.buttonMusica, self.abrir_music_screen),
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
        button.bind("<FocusIn>", lambda event: self.on_enter(event, button))
        button.bind("<FocusOut>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(width=self.button_width + 20, height=self.button_height + 20, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(width=self.button_width, height=self.button_height, fg='white')

    def limpiar_panel(self, panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_music_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        MusicScreen(self.cuerpo_principal, self.app_logic)

    def abrir_images_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        ImagesScreen(self.cuerpo_principal, self.app_logic)

    def abrir_video_options_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        VideoOptions(self.cuerpo_principal, self.app_logic)
