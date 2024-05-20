import os
import tkinter as tk
import vlc

class VideoFrame:
    def __init__(self, panel_principal, app_logic, video_files):
        self.panel_principal = panel_principal
        self.app_logic = app_logic
        self.video_files = video_files
        self.current_video_index = 0
        self.player = vlc.MediaPlayer()

        self.instance = vlc.Instance()  # Inicializar la instancia de VLC

        self.video_panel = tk.Frame(self.panel_principal, bg="black")
        self.video_panel.pack(side=tk.TOP, fill="both", expand=True)

        self.detenerButton = tk.Button(self.panel_principal, text="Detener", font=("Roboto", 20), command=self.regresar)
        self.detenerButton.pack(side=tk.TOP, padx=10, pady=10)

        self.play_video()

    def play_video(self):
        len(self.video_files)
        selected_video = self.video_files[self.current_video_index]
        video_path = os.path.join("/home/pi/usb", selected_video)

        # self.player.stop()  # Detener la reproducción actual

        media = self.instance.media_new(video_path)
        self.player.set_media(media)

        handle = self.video_panel.winfo_id()
        self.player.set_xwindow(handle)

        self.player.play()

        # Conectar evento de fin de reproducción
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end)

    def on_end(self, event):
        print("On end")
        self.current_video_index = (self.current_video_index + 1) % len(self.video_files)
        self.play_video()

    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def regresar(self):
        self.player.stop()
        self.limpiar_panel(self.panel_principal)     
        HomeScreen(self.panel_principal, self.app_logic)
