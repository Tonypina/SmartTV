import tkinter as tk
from tkinter import ttk, filedialog

class SmartTVAppGUI:
    def __init__(self, root, app_logic):
        self.root = root
        self.app_logic = app_logic

        # Configuración de la ventana principal
        self.root.title("Smart TV Interface")
        self.root.attributes('-fullscreen', True)

        # Crear el sidebar
        self.sidebar = ttk.Frame(root, width=200, relief="raised", padding=(10, 10))
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Crear los botones del sidebar
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home)
        self.home_button.grid(row=0, column=0, sticky="ew", pady=5)
        self.network_button = ttk.Button(self.sidebar, text="Red", command=self.show_network)
        self.network_button.grid(row=1, column=0, sticky="ew", pady=5)

        # Inicializar el área de contenido
        self.content_area = ttk.Frame(root, relief="raised", padding=(10, 10))
        self.content_area.grid(row=0, column=1, sticky="nsew")

        # Mostrar la interfaz de inicio por defecto
        self.show_home()

    def show_home(self):
        # Limpiar el área de contenido
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Crear y mostrar la interfaz de inicio
        self.home_label = ttk.Label(self.content_area, text="Interfaz de Inicio")
        self.home_label.pack(expand=True, fill="both")

    def show_network(self):
        # Limpiar el área de contenido
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Mostrar las redes disponibles
        available_networks = self.app_logic.display_available_networks()
        if available_networks:
            self.network_label = ttk.Label(self.content_area, text="Redes Disponibles:")
            self.network_label.pack(expand=True, fill="both")

            # Crear y mostrar los botones para las redes disponibles
            for network in available_networks:
                network_button = ttk.Button(self.content_area, text=network, command=lambda n=network: self.connect_to_network(n))
                network_button.pack(expand=True, fill="both")

            # Agregar un campo de entrada para la contraseña
            self.password_entry = ttk.Entry(self.content_area, show="*")
            self.password_entry.pack(expand=True, fill="both")

            # Botón para conectar a la red seleccionada
            connect_button = ttk.Button(self.content_area, text="Conectar", command=self.connect_to_selected_network)
            connect_button.pack(expand=True, fill="both")
        else:
            no_networks_label = ttk.Label(self.content_area, text="No se encontraron redes disponibles")
            no_networks_label.pack(expand=True, fill="both")

    def connect_to_network(self, network):
        # Al seleccionar una red, mostrar el nombre de la red seleccionada
        self.selected_network_label = ttk.Label(self.content_area, text=f"Conectar a la red: {network}")
        self.selected_network_label.pack(expand=True, fill="both")

        # Guardar el nombre de la red seleccionada
        self.selected_network = network

    def connect_to_selected_network(self):
        # Obtener la contraseña ingresada por el usuario
        password = self.password_entry.get()

        # Conectar a la red seleccionada con la contraseña proporcionada
        if hasattr(self, "selected_network") and password:
            self.app_logic.connect_to_network(self.selected_network, password)

# Clase para la lógica de la aplicación
class SmartTVAppLogic:
    def display_available_networks(self):
        # Simulación de búsqueda de redes disponibles
        return ["Red1", "Red2", "Red3"]

    def connect_to_network(self, network, password):
        # Simulación de conexión a una red
        print(f"Conectando a la red '{network}' con la contraseña '{password}'")

