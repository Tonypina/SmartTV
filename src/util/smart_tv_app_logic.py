import os
import time
import threading
import vlc
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk

class SmartTVAppLogic:
    def __init__(self, screen_width, screen_height):
        self.media_player = None
        self.media_thread = None
        self.screen_width = screen_width + 1
        self.screen_height = screen_height

    def open_netflix_kiosk(self): 
        url_servicios_video = "https://www.netflix.com"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")

    def open_youtube_kiosk(self):
        url_servicios_video = "https://www.youtube.com"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")

    def open_google_kiosk(self):
        url_servicios_video = "https://www.google.com"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")

    def open_spotify_kiosk(self):
        url_servicios_video = "https://open.spotify.com/"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")

    def open_hbo_kiosk(self):
        url_servicios_video = "https://www.max.com/mx/es"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")
    
    def open_f1_kiosk(self):
        url_servicios_video = "https://f1tv.formula1.com/"
        os.system(f"chromium-browser --start-fullscreen --hide-scrollbars --enable-chrome-browser-cloud-management --window-size={self.screen_width},{self.screen_height} --window-position=0,0 --app={url_servicios_video}")

    def get_wifi_ssids(self):
        # Ejecuta el comando para listar las redes Wi-Fi disponibles
        resultado = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
        
        # Verifica si el comando se ejecutó correctamente
        if resultado.returncode != 0:
            raise Exception("Error al ejecutar el comando de red")

        # Divide la salida del comando en líneas y filtra líneas vacías
        lineas = [linea.strip() for linea in resultado.stdout.split('\n') if linea.strip()]
        
        # Inicializa una lista para almacenar las redes encontradas
        redes = []

        # Recorre las líneas y agrega las redes a la lista
        for linea in lineas:
            redes.append(linea)

        return redes

    def connect_to_network(self, network, password):
        # Simulación de conexión a una red
        print(f"Conectando a la red '{network}' con la contraseña '{password}'")

    def usb_inserted(self):
        
        type = self.mount_usb()
        
        if type > 0:
            return type
        else:
            print("Failed to mount the USB device")
            return None

    def mount_usb(self):
        usb_path = "/home/pi/usb"
        try:
            result = subprocess.run(['sudo', 'mount', '/dev/sda1', usb_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:

                type = self.analyze_usb_content(usb_path)
                return type
            else:
                print(f"Error mounting USB: {result.stderr.decode('utf-8')}")
                return None
        except Exception as e:
            print(f"Exception mounting USB: {e}")
            return None

    def umount_usb(self):
        try:
            result = subprocess.run(['sudo', 'umount', '/dev/sda1'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                return True
            else:
                print(f"Error umounting USB: {result.stderr.decode('utf-8')}")
                return False
        except Exception as e:
            print(f"Exception umounting USB: {e}")
            return False

    def analyze_usb_content(self, usb_path):
        video_ext = ('.mp4', '.avi', '.mov', '.mkv')
        image_ext = ('.jpg', '.jpeg', '.png', '.gif')
        music_ext = ('.mp3', '.wav', '.aac', '.flac')

        video_files = []
        image_files = []
        music_files = []

        for root, _, files in os.walk(usb_path):
            for file in files:
                if file.endswith(video_ext):
                    video_files.append(os.path.join(root, file))
                elif file.endswith(image_ext):
                    image_files.append(os.path.join(root, file))
                elif file.endswith(music_ext):
                    music_files.append(os.path.join(root, file))

        if len(video_files) and not len(image_files) and not len(music_files):
            return 0
        elif len(image_files) and not len(video_files) and not len(music_files):
            return 1
        elif len(music_files) and not len(video_files) and not len(image_files):
            return 2
        else:
            return 3