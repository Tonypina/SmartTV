import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_imagenes as util_img
from util.smart_tv_app_logic import SmartTVAppLogic
import threading
import pyudev

# Nuevo
from gui.home_screen import HomeScreen
from gui.network_screen import NetworkScreen
from gui.video_options_screen import VideoScreen
from gui.images_screen import ImagesScreen
from gui.music_screen import MusicScreen
from gui.mixto_screen import MixtoScreen

class SmartTVAppGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        # self.logo = util_img.leer_imagen("./src/img/logo.png", (560, 136))
        # self.perfil = util_img.leer_imagen("./src/img/Perfil.png", (100, 100))
        # self.img_sitio_construccion = util_img.leer_imagen("./src/img/sitio_construccion.png", (200, 200))
        # self.bind('<KeyPress>', self.handle_keypress)

        self.app_logic = SmartTVAppLogic(self.winfo_screenwidth(), self.winfo_screenheight())

        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo(self.app_logic)
        # self.bind('<Escape>', self.exit_app)

        # Iniciar el hilo para detectar la inserción de USB
        self.usb_monitor_thread = threading.Thread(target=self.monitor_usb)
        self.usb_monitor_thread.daemon = True
        self.usb_monitor_thread.start()
    
    def config_window(self):
        # Configuración inicial de la ventana
        pantall_ancho = self.winfo_screenwidth()
        pantall_largo = self.winfo_screenheight()
        self.geometry(f"{pantall_ancho}x{pantall_largo}")

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=250)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="MaFE TV")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Piña San Miguel Colón")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 30
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        # Botones del menú lateral
        self.buttonHome = tk.Button(self.menu_lateral)        
        self.buttonUSB = tk.Button(self.menu_lateral)
        self.buttonNetwork = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Home", "\uf109", self.buttonHome, self.abrir_home_screen ),
            ("Reproducir disco extraible", "\uf013", self.buttonUSB, self.abrir_mixto_screen),
            ("Configuración de Red", "\uf013", self.buttonNetwork, self.abrir_network_screen),
        ]

        for text, icon, button,comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu,comando)                    
    
    def controles_cuerpo(self, app_logic):
        HomeScreen(self.cuerpo_principal, app_logic)
  
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"      {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command = comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
    # Nuevo
    def abrir_home_screen(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        HomeScreen(self.cuerpo_principal, self.app_logic)   
        
    def abrir_network_screen(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        NetworkScreen(self.cuerpo_principal, self.app_logic) 
        
    def abrir_usb_screen(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        USBScreen(self.cuerpo_principal, self.app_logic) 

    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def exit_app(self, event=None):
        self.app_logic.umount_usb()
        self.destroy()

    def monitor_usb(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        for device in iter(monitor.poll, None):
            if device.action == 'add':
                self.after(3000, self.usb_inserted)

    def usb_inserted(self):
        type = self.app_logic.usb_inserted()

        if (type) :
            if (type == 0):
                self.abrir_video_options_screen()
            elif (type == 1):
                self.abrir_images_screen()
            elif (type == 2):
                self.reproduce_music()
            elif (type == 3):
                self.abrir_mixto_screen()
        else:
            print("Error al leer la USB")

    def abrir_video_options_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        VideoOptions(self.cuerpo_principal, self.app_logic)
    
    def abrir_images_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        ImagesScreen(self.cuerpo_principal, self.app_logic)
    
    def reproduce_music(self):
        self.limpiar_panel(self.cuerpo_principal)     
        MusicScreen(self.cuerpo_principal, self.app_logic)
    
    def abrir_mixto_screen(self):
        self.limpiar_panel(self.cuerpo_principal)     
        MixtoScreen(self.cuerpo_principal, self.app_logic)