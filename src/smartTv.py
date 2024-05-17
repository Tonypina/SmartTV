import os
import time
import threading
import vlc
from tkinter import filedialog
from PIL import Image, ImageTk

class SmartTV:
    def __init__(self):
        self.media_player = None
        self.media_thread = None

    def open_netflix_kiosk(self):
        url_servicios_video = "https://www.netflix.com"
        os.system(f"chromium-browser --no-sandbox --kiosk {url_servicios_video}")

    def open_youtube_kiosk(self):
        url_servicios_video = "https://www.youtube.com"
        os.system(f"chromium-browser --no-sandbox --kiosk {url_servicios_video}")

    def open_google_kiosk(self):
        url_servicios_video = "https://www.google.com"
        os.system(f"chromium-browser --no-sandbox --kiosk {url_servicios_video}")

    def play_usb_content(self, root):
        usb_path = filedialog.askdirectory(title="Seleccionar USB")
        if usb_path:
            self.stop_media_player()  # Detener la reproducción actual si la hay
            self.show_usb_content_interface(root, usb_path)

    def play_vlc_content(self, root):
        self.stop_media_player()  # Detener la reproducción actual si la hay
        media_path = filedialog.askopenfilename(title="Seleccionar archivo multimedia",
                                                filetypes=(("Archivos multimedia", "*.mp4;*.avi;*.mkv"), ("Todos los archivos", "*.*")))
        if media_path:
            self.play_video(media_path)

    def show_usb_content_interface(self, root, usb_path):
        # Crear una nueva ventana para la interfaz de contenido USB
        usb_content_window = tk.Toplevel(root)
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
        play_image_button = ttk.Button(usb_content_window, text="Reproducir Imágenes", command=lambda: self.play_media_files(image_listbox.get(tk.ACTIVE), usb_path, "image", root))
        play_image_button.pack(pady=10)

        play_audio_button = ttk.Button(usb_content_window, text="Reproducir Música", command=lambda: self.play_media_files(audio_listbox.get(tk.ACTIVE), usb_path, "audio"))
        play_audio_button.pack(pady=10)

        play_video_button = ttk.Button(usb_content_window, text="Reproducir Video", command=lambda: self.play_media_files(video_listbox.get(tk.ACTIVE), usb_path, "video"))
        play_video_button.pack(pady=10)

        # Botón para salir de la interfaz de contenido USB
        back_button = ttk.Button(usb_content_window, text="Volver al Menú Principal", command=usb_content_window.destroy)
        back_button.pack(pady=10)

    def play_media_files(self, media_file, usb_path, media_type, root):
        if not media_file:
            return

        media_path = os.path.join(usb_path, media_file)
        self.stop_media_player()  # Detener la reproducción actual si la hay

        if media_type == "image":
            self.play_slideshow(usb_path, [media_file], root)
        elif media_type == "audio":
            self.play_audio(media_path)
        elif media_type == "video":
            self.play_video(media_path)

    def play_slideshow(self, usb_path, image_files, root):
        # Reproducir imágenes en modo presentación
        for img_file in image_files:
            img_path = os.path.join(usb_path, img_file)
            img = Image.open(img_path)
            img = img.resize((root.winfo_width(), root.winfo_height()), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            root.configure(image=img)
            root.image = img
            root.update()
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

    def stop_media_player(self):
        if self.media_player:
            self.media_player.stop()
            if self.media_thread:
                self.media_thread.join()
                self.media_thread = None
