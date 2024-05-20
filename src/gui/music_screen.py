import tkinter as tk
from tkinter import ttk
import os
import pygame

# Configuración de color (puedes ajustar según tus necesidades)
COLOR_CUERPO_PRINCIPAL = "#ffffff"

class MusicScreen:

    def __init__(self, panel_principal, app_logic):
        self.panel_principal = panel_principal
        self.app_logic = app_logic

        # Inicializar pygame mixer
        pygame.init()
        pygame.mixer.init()

        # Crear paneles: barra sup
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Crear paneles: barra inf
        self.barra_inf = tk.Frame(panel_principal)
        self.barra_inf.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_sup, text="Reproducción de Música")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Lista de archivos de música
        self.music_files = self.load_music_from_directory('/home/pi/usb')
        self.current_music_index = 0

        # Iniciar la reproducción de música
        self.play_next_song()

    def load_music_from_directory(self, directory):
        supported_formats = ('.mp3', '.wav', '.ogg', '.flac')
        files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(supported_formats)]
        return files

    def play_next_song(self):
        if self.music_files:
            music_path = self.music_files[self.current_music_index]

            # Cargar y reproducir la canción
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            # Incrementar el índice de la canción actual
            self.current_music_index = (self.current_music_index + 1) % len(self.music_files)

            # Configurar evento para cuando termine la canción
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.panel_principal.after(100, self.check_music_end)
        else:
            self.labelTitulo.config(text="No hay archivos de música en el directorio especificado")

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_song()
        self.panel_principal.after(100, self.check_music_end)
