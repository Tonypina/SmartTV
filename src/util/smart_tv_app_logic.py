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

    def play_usb_content(self):
        usb_path = filedialog.askdirectory(title="Seleccionar USB")
        if usb_path:
            self.stop_media_player()  # Detener la reproducción actual si la hay
            self.show_usb_content_interface(usb_path)

    def play_vlc_content(self):
        self.stop_media_player()  # Detener la reproducción actual si la hay
        media_path = filedialog.askopenfilename(title="Seleccionar archivo multimedia",
                                                 filetypes=(("Archivos multimedia", "*.mp4;*.avi;*.mkv"), ("Todos los archivos", "*.*")))
        if media_path:
            self.play_video(media_path)

    def stop_media_player(self):
        if self.media_player:
            self.media_player.stop()
            if self.media_thread:
                self.media_thread.join()
                self.media_thread = None

    def show_usb_content_interface(self, usb_path):
        # Crear una nueva ventana para la interfaz de contenido USB
        usb_content_window = tk.Toplevel(self.root)
        usb_content_window.title("Contenido USB")
        usb_content_window.geometry("1600x900")

        # Obtener lista de archivos en la memoria USB
        usb_files = os.listdir(usb_path)

        # Filtrar archivos multimedia (imágenes, música, videos)
        image_files = [f for f in usb_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        audio_files = [f for f in usb_files if f.lower().endswith(('.mp3', '.wav', '.flac'))]
        video_files = [f for f in usb_files if f.lower().endswith(('.mp4', '.avi', '.mkv'))]

        # Crear listas con nombres de archivos
        image_listbox = tk.Listbox(usb_content_window, selectmode=tk.SINGLE)
        for img in image_files:
            image_listbox.insert(tk.END, img)
        image_listbox.pack(pady=10)

        audio_listbox = tk.Listbox(usb_content_window, selectmode=tk.SINGLE)
        for audio in audio_files:
            audio_listbox.insert(tk.END, audio)
        audio_listbox.pack(pady=10)

        video_listbox = tk.Listbox(usb_content_window, selectmode=tk.SINGLE)
        for video in video_files:
            video_listbox.insert(tk.END, video)
        video_listbox.pack(pady=10)

        # Botones para reproducir el contenido seleccionado
        play_image_button = ttk.Button(usb_content_window, text="Reproducir Imágenes", command=lambda: self.play_media_files(image_listbox.get(tk.ACTIVE), usb_path, "image"))
        play_image_button.pack(pady=10)

        play_audio_button = ttk.Button(usb_content_window, text="Reproducir Música", command=lambda: self.play_media_files(audio_listbox.get(tk.ACTIVE), usb_path, "audio"))
        play_audio_button.pack(pady=10)

        play_video_button = ttk.Button(usb_content_window, text="Reproducir Video", command=lambda: self.play_media_files(video_listbox.get(tk.ACTIVE), usb_path, "video"))
        play_video_button.pack(pady=10)

        # Botón para salir de la interfaz de contenido USB
        back_button = ttk.Button(usb_content_window, text="Volver al Menú Principal", command=usb_content_window.destroy)
        back_button.pack(pady=10)

    def play_media_files(self, media_file, usb_path, media_type):
        if not media_file:
            return

        media_path = os.path.join(usb_path, media_file)
        self.stop_media_player()  # Detener la reproducción actual si la hay

        if media_type == "image":
            image_files = [f for f in os.listdir(usb_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.play_slideshow(usb_path, image_files)
        elif media_type == "audio":
            self.play_audio(media_path)
        elif media_type == "video":
            self.play_video(media_path)

    def play_slideshow(self, usb_path, image_files):
        # Reproducir imágenes en modo presentación
        for img_file in image_files:
            img_path = os.path.join(usb_path, img_file)
            img = Image.open(img_path)
            img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.bg_label.configure(image=img)
            self.bg_label.image = img
            self.root.update()
            time.sleep(5)

    def play_audio(self, audio_path):
        # Reproducir música en bucle infinito
        self.media_player = vlc.MediaPlayer(audio_path)
        self.media_player.play()
        self.media_thread = threading.Thread(target=self.media_player_listener)
        self.media_thread.start()

    def play_video(self, video_path):
        self.media_player = vlc.MediaPlayer(video_path)
        self.media_player.play()
        self.media_thread = threading.Thread(target=self.media_player_listener)
        self.media_thread.start()

    def media_player_listener(self):
        while True:
            if self.media_player.get_state() == vlc.State.Ended:
                self.stop_media_player()
                break
            time.sleep(1)

    def display_available_networks(self):
        import subprocess

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

    def usb_inserted(self, device_node):
        
        mount_path = self.mount_usb(device_node)
        print(mount_path)
        # if mount_path:
        #     self.analyze_usb_content(mount_path)
        # else:
        #     print("Failed to mount the USB device")

    def mount_usb(self, device_node):
        mount_point = f"/mnt/{os.path.basename(partition)}"
        os.makedirs(mount_point, exist_ok=True)
        try:
            subprocess.run(['mount', partition, mount_point], check=True)
            print(f"Mounted {partition} at {mount_point}")
            return mount_point
            # self.check_usb_content(mount_point)
        except subprocess.CalledProcessError as e:
            print(f"Error mounting USB: {e}")

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

        if video_files and not image_files and not music_files:
            self.show_video_options(video_files)
        elif image_files and not video_files and not music_files:
            self.show_image_slideshow(image_files)
        elif music_files and not video_files and not image_files:
            self.play_music_playlist(music_files)
        else:
            self.ask_user_action(video_files, image_files, music_files)