import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import time

class SmartTVAppGUI:
    def __init__(self, root, app_logic):
        self.root = root
        self.app_logic = app_logic
        self.root.title("Smart TV Interface")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_app)
        self.root.bind('<Control-q>', self.exit_app)

        # Obtener la resolución del monitor
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.screen_width, self.screen_height))


        # Inicializar variables para el fondo
        self.bg_paths = ["background1.jpg", "background2.jpg", "background3.jpg"]
        self.bg_images = [self.load_image(path, self.screen_width, self.screen_height) for path in self.bg_paths]
        self.current_bg_index = 0
        self.bg_label = tk.Label(root)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.resize_background)
        self.update_background()

        self.buttons = []
        self.create_home_buttons()

        # Configurar la geometría de la ventana
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(list(range(len(self.buttons)+2)), weight=1)

        # Crear botones de acceso (Home)
        
        # Crear el sidebar
        self.sidebar = ttk.Frame(self.root, height=self.screen_height, relief="raised", padding=(10, 10))
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Crear los botones del sidebar
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home)
        self.home_button.grid(row=0, column=0, sticky="ew", pady=5)
        self.network_button = ttk.Button(self.sidebar, text="Red", command=self.show_network)
        self.network_button.grid(row=1, column=0, sticky="ew", pady=5)


        # Establecer estilos para los botones
        style = ttk.Style()
        style.configure("WhiteButton.TButton", background="white", foreground="black", bordercolor="white")

        # Añadir título en la parte superior izquierda
        title_label = tk.Label(root, text="MaFE TV", font=("Helvetica", 30), fg="black", bg=root.cget("bg"))
        title_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Añadir la hora en la parte superior derecha
        self.time_label = tk.Label(root, text="", font=("Helvetica", 24), fg="black", bg=root.cget("bg"))
        self.time_label.grid(row=0, column=len(self.buttons), padx=10, pady=10, sticky="e")
        self.update_time()

        # Estado para rastrear la posición actual del cursor
        self.current_button_index = 0

        # Lógica para manejar la entrada del teclado universal
        self.root.bind('<KeyPress>', self.handle_keypress)

        # Configurar estilos para los botones seleccionados
        style.configure("SelectedButton.TButton", background="yellow", foreground="black", bordercolor="white")

    def create_home_buttons(self):
        # Crear botones de acceso (Home)
        buttons_info = [
            {"name": "Netflix", "icon": "netflix.png", "command": self.app_logic.open_netflix_kiosk},
            {"name": "YouTube", "icon": "youtube.png", "command": self.app_logic.open_youtube_kiosk},
            {"name": "Google", "icon": "google.png", "command": self.app_logic.open_google_kiosk},
            {"name": "Reproducir", "icon": "usb.png", "command": self.app_logic.play_usb_content},
            {"name": "Reproducir con VLC", "icon": "vlc.png", "command": self.app_logic.play_vlc_content}
        ]

        for i, button_info in enumerate(buttons_info):
            button = ttk.Button(self.root, text=button_info["name"], compound=tk.TOP, style="WhiteButton.TButton",
                                command=button_info["command"])
            button.image = self.load_image(button_info["icon"], 100, 100)
            button.config(image=button.image)
            button.grid(row=2, column=i+1, padx=10, pady=10)
            self.buttons.append(button)

    def show_home(self):
        # Limpiar el área de contenido
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el sidebar
        self.sidebar = ttk.Frame(self.root, relief="raised", padding=(10, 10))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.root.update_idletasks()  # Asegurar que el sidebar tenga la altura completa del monitor

        # Crear los botones del sidebar
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home)
        self.home_button.grid(row=0, column=0, sticky="ew", pady=(self.screen_height // 2 - 100, 5))  # Centrar verticalmente
        self.network_button = ttk.Button(self.sidebar, text="Red", command=self.show_network)
        self.network_button.grid(row=1, column=0, sticky="ew", pady=5)  # Ajustar el espaciado

        # Mostrar los botones de acceso para la página de inicio (Home)
        self.create_home_buttons()

        self.update_background()  # Actualizar el fondo

    def show_network(self):
        # Limpiar el área de contenido
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el sidebar
        self.sidebar = ttk.Frame(self.root, relief="raised", padding=(10, 10))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.root.update_idletasks()  # Asegurar que el sidebar tenga la altura completa del monitor

        # Crear los botones del sidebar
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home)
        self.home_button.grid(row=0, column=0, sticky="ew", pady=(self.screen_height // 2 - 100, 5))  # Centrar verticalmente
        self.network_button = ttk.Button(self.sidebar, text="Red", command=self.show_network)
        self.network_button.grid(row=1, column=0, sticky="ew", pady=5)  # Ajustar el espaciado

        # Mostrar la lista de redes disponibles
        self.app_logic.display_available_networks()

        # Crear un entry para que el usuario escriba la contraseña
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Crear un botón para conectarse a la red seleccionada
        connect_button = ttk.Button(self.root, text="Conectar", command=self.connect_to_network)
        connect_button.grid(row=2, column=2, padx=10, pady=10)

        self.update_background()  # Actualizar el fondo


    def connect_to_network(self):
        # Obtener la red seleccionada y la contraseña ingresada
        selected_network = self.app_logic.selected_network.get()
        password = self.password_entry.get()

        # Llamar al método para conectarse a la red
        self.app_logic.connect_to_network(selected_network, password)

    def resize_background(self, event):
        img = self.bg_images[self.current_bg_index]
        img = img.resize((event.width, event.height), Image.ANTIALIAS)
        self.bg_images[self.current_bg_index] = ImageTk.PhotoImage(img)
        self.bg_label.configure(image=self.bg_images[self.current_bg_index])

    def update_background(self):
        self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_images)
        self.bg_label.configure(image=self.bg_images[self.current_bg_index])
        self.root.after(5000, self.update_background)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def load_image(self, path, width, height):
        img = Image.open(path)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def handle_keypress(self, event):
        key = event.keysym.lower()

        if key == 'a':
            self.move_left()
        elif key == 'd':
            self.move_right()
        elif key == 'w':
            self.move_up()
        elif key == 's':
            self.move_down()
        elif key == 'return':
            self.select_application()
        elif key == 'm':
            self.app_logic.show_media_player_interface()
        elif key == 'q':
            if self.app_logic.media_player:
                self.app_logic.stop_media_player()
                self.root.deiconify()  # Mostrar la ventana principal después de salir del reproductor multimedia

    def move_left(self):
        self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
        self.highlight_current_button()

    def move_right(self):
        self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
        self.highlight_current_button()

    def move_up(self):
        self.current_button_index = (self.current_button_index - len(self.buttons)) % len(self.buttons)
        self.highlight_current_button()

    def move_down(self):
        self.current_button_index = (self.current_button_index + len(self.buttons)) % len(self.buttons)
        self.highlight_current_button()

    def select_application(self):
        selected_button = self.buttons[self.current_button_index]
        selected_button.invoke()

    def highlight_current_button(self):
        for i, button in enumerate(self.buttons):
            if i == self.current_button_index:
                button.configure(style="SelectedButton.TButton")
            else:
                button.configure(style="WhiteButton.TButton")

    def exit_app(self, event=None):
        self.app_logic.stop_media_player()  # Detener la reproducción antes de salir
        self.root.destroy()


