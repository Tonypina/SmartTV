import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA


class ImagesScreen:

    def __init__(self, panel_principal, app_logic):
        self.panel_principal = panel_principal
        self.app_logic = app_logic

        # Crear paneles: barra sup
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Crear paneles: barra inf
        self.barra_inf = tk.Frame(panel_principal)
        self.barra_inf.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_sup, text="Presentación de Imágenes en USB")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Label para mostrar imágenes
        self.image_label = tk.Label(self.barra_inf)
        self.image_label.pack(side=tk.TOP, fill='both', expand=True)

        # Lista de imágenes
        self.image_files = self.load_images_from_directory('/home/pi/usb')
        self.current_image_index = 0

        # Iniciar la presentación de imágenes
        self.show_next_image()

    def load_images_from_directory(self, directory):
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(supported_formats)]
        return files

    def show_next_image(self):
        if self.image_files:
            image_path = self.image_files[self.current_image_index]
            image = Image.open(image_path)
            image = image.resize((self.panel_principal.winfo_width(), self.panel_principal.winfo_height()), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)

            # Cambiar imagen cada 3 segundos (3000 ms)
            self.panel_principal.after(3000, self.show_next_image)
        else:
            self.labelTitulo.config(text="No hay imágenes en el directorio especificado")
