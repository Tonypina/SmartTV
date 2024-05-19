import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from util.smart_tv_app_logic import SmartTVAppLogic

class HomeScreen():

    def __init__(self, panel_principal, app_logic):
        
        button_width = 20
        button_height = 2
        button_font = font.Font(family='FontAwesome', size=15)
        
        self.buttonNetflix = tk.Button( panel_principal )

        buttons_info = [
            ("Netflix", self.buttonNetflix, app_logic.open_netflix_kiosk)
        ]

        for text, button, command in buttons_info:
            self.buttons_config(text, button, button_font, button_width, button_height, command)

        # Crear paneles: barra superior
        # self.barra_superior = tk.Frame( panel_principal)
        # self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # # Crear paneles: barra inferior
        # self.barra_inferior = tk.Frame( panel_principal)
        # self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # # Primer Label con texto
        # self.labelTitulo = tk.Label(
        #     self.barra_superior, text="Página en construcción")
        # self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        # self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # # Segundo Label con la imagen
        # self.label_imagen = tk.Label(self.barra_inferior, image=logo)
        # self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        # self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_CUERPO_PRINCIPAL)

    def buttons_config(self, text, button, button_font, button_width, button_height, command):
        button.config(text=f"{text}", anchor="center", font=button_font,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=button_width, height=button_height,
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