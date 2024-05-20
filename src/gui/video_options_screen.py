import os
import tkinter as tk
from tkinter import ttk
import vlc

from gui.video_frame import VideoFrame

def get_video_files(directory="/home/pi/usb"):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in video_extensions]

class VideoScreen:
    def __init__(self, panel_principal, app_logic):
        self.panel_principal = panel_principal
        self.app_logic = app_logic

        self.video_files = get_video_files()

        # Crear paneles: barra superior
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Crear paneles: barra inferior
        self.barra_inf = tk.Frame(panel_principal)
        self.barra_inf.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Título
        self.labelTitulo = tk.Label(self.barra_sup, text="Selecciona un Video")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Crear botones para cada video
        for video in self.video_files:
            self.create_video_button(video)

    def create_video_button(self, video):
        button = tk.Button(self.barra_inf, text=video, font=("Roboto", 20), command=lambda: self.abrir_video_frame(video))
        button.pack(fill=tk.X, pady=5)

    def limpiar_panel(self, panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_video_frame(self, video):
        self.limpiar_panel(self.panel_principal)
        VideoFrame(self.panel_principal, self.app_logic, video)

