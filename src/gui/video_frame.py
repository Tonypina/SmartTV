import os
import tkinter as tk
from tkinter import ttk
import vlc
import time

from gui.home_screen import HomeScreen

class VideoFrame:
    def __init__(self, panel_principal, app_logic, video_files):
        self.panel_principal = panel_principal
        self.app_logic = app_logic
        self.video_files = video_files
        self.current_video_index = 0
        self.player = vlc.MediaPlayer()
                
        # Inicializar VLC player para integrar con tkinter
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Área de video
        self.video_panel = tk.Frame(self.panel_principal, bg="black")
        self.video_panel.pack(side=tk.TOP, fill="both", expand=True)

        self.detenerButton = tk.Button(self.panel_principal, text="Detener", font=("Roboto", 20), command=self.regresar)
        self.detenerButton.pack(side=tk.TOP, padx=10, pady=10)

        # Conectar evento de fin de reproducción
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end)

        self.play_video()

    def play_video(self):
        selected_video = self.video_files[self.current_video_index]
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

    def on_end(self, event):
        # Incrementar el índice del video
        self.current_video_index = (self.current_video_index + 1) % len(self.video_files)
        # Reproducir el siguiente video
        self.play_video()

    def limpiar_panel(self, panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def regresar(self):
        self.player.stop()
        self.limpiar_panel(self.panel_principal)     
        HomeScreen(self.panel_principal, self.app_logic)
