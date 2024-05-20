import os
import tkinter as tk
from tkinter import ttk
import vlc

def get_video_files(directory="/home/pi/usb"):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in video_extensions]

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

        # Vincular la tecla Escape para salir de pantalla completa
        # self.panel_principal.bind("<Escape>", self.exit_fullscreen)

    def play_video(self):
        selected_video_index = self.video_listbox.curselection()
        if not selected_video_index:
            return
        
        selected_video = self.video_file
        video_path = os.path.join("/home/pi/usb", selected_video)

        # Detener el video actual si está reproduciéndose
        self.player.stop()

        # Crear un nuevo media y reproducirlo
        media = self.instance.media_new(video_path)
        self.player.set_media(media)

        # Configurar el panel de video en el tkinter frame
        handle = self.video_panel.winfo_id()
        self.player.set_hwnd(handle)

        # Reproducir el video
        self.player.play()
