import os
import tkinter as tk
from tkinter import ttk
import vlc
import time

from gui.home_screen import HomeScreen

class VideoFrame:
    def __init__(self, panel_principal, app_logic, video_file):
        self.panel_principal = panel_principal
        self.app_logic = app_logic
        self.video_file = video_file
        self.player = vlc.MediaPlayer()
                
        # Inicializar VLC player para integrar con tkinter
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Área de video
        self.video_panel = tk.Frame(self.panel_principal, bg="black")
        self.video_panel.pack(side=tk.TOP, fill="both", expand=True)

        self.play_video()

        # Vincular la tecla Escape para salir de pantalla completa
        self.panel_principal.bind("<x>", self.regresar)

    def play_video(self):
        
        selected_video = self.video_file
        video_path = os.path.join("/home/pi/usb", selected_video)

        # Detener el video actual si está reproduciéndose
        self.player.stop()

        # Crear un nuevo media y reproducirlo
        media = self.instance.media_new(video_path)
        self.player.set_media(media)

        # Configurar el panel de video en el tkinter frame
        handle = self.video_panel.winfo_id()
        self.player.set_xwindow(handle)

        # Reproducir el video
        self.player.play()

    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def regresar(self):
        
        self.player.stop()

        self.limpiar_panel(self.panel_principal)     
        HomeScreen(self.panel_principal, self.app_logic)


