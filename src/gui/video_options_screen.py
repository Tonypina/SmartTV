import os
import tkinter as tk
from tkinter import ttk
import vlc

def get_video_files(directory="/home/pi/usb"):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in video_extensions]

class VideoScreen:
    def __init__(self, panel_principal, app_logic):
        self.panel_principal = panel_principal
        self.app_logic = app_logic
        self.player = vlc.MediaPlayer()
        self.is_fullscreen = False

        self.video_files = get_video_files()

        # Crear paneles: barra superior
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Crear paneles: barra izquierda
        self.barra_izq = tk.Frame(panel_principal)
        self.barra_izq.pack(side=tk.LEFT, fill="both", expand=True)

        # Crear paneles: barra derecha
        self.barra_der = tk.Frame(panel_principal)
        self.barra_der.pack(side=tk.RIGHT, fill="both", expand=True)

        # Título
        self.labelTitulo = tk.Label(self.barra_sup, text="Selecciona un Video")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Lista de videos
        self.video_listbox = tk.Listbox(self.barra_izq, font=("Roboto", 20))
        self.video_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        for video in self.video_files:
            self.video_listbox.insert(tk.END, video)

        # Botón de reproducir
        self.play_button = tk.Button(self.barra_der, text="Reproducir", font=("Roboto", 20), command=self.play_video)
        self.play_button.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Botón de salir de pantalla completa
        self.exit_button = tk.Button(self.barra_der, text="Salir de Pantalla Completa", font=("Roboto", 20), command=self.exit_fullscreen)
        self.exit_button.pack(side=tk.TOP, fill='both', expand=True)
        self.exit_button.pack_forget()  # Ocultar el botón al inicio

        # Inicializar VLC player para integrar con tkinter
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Vincular la tecla Escape para salir de pantalla completa
        self.panel_principal.bind("<Escape>", self.exit_fullscreen)

    def limpiar_panel(self, panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_video_frame(self):
        self.limpiar_panel(self.panel_principal)     
        VideoFrame(self.panel_principal, self.app_logic, self.video_files[selected_video_index[0]])