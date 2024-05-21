import tkinter as tk
from config import COLOR_CUERPO_PRINCIPAL

class NetworkScreen:
    def __init__(self, panel_principal, app_logic):
        self.app_logic = app_logic
        self.wifi_ssids = app_logic.get_wifi_ssids()

        # Crear paneles: barra sup
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False) 
        
        # Crear paneles: barra izquierda
        self.barra_izq = tk.Frame(panel_principal)
        self.barra_izq.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_izq.pack(side=tk.LEFT, fill="both", expand=True) 

        # Crear paneles: barra derecha
        self.barra_der = tk.Frame(panel_principal)
        self.barra_der.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_der.pack(side=tk.RIGHT, fill="both", expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(self.barra_sup, text="Configuración de Red")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=50)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        self.selectedSSIDLabel = tk.Label(self.barra_der, text="SSID: ")
        self.selectedSSIDLabel.config(fg="#222d33", font=("Roboto", 20), padx=10, width=20, bg=COLOR_CUERPO_PRINCIPAL)
        self.selectedSSIDLabel.pack(side=tk.TOP)

        self.passwordLabel = tk.Label(self.barra_der, text="Contraseña:")
        self.passwordLabel.config(fg="#222d33", font=("Roboto", 20), padx=10, width=20, bg=COLOR_CUERPO_PRINCIPAL)
        self.passwordLabel.pack(side=tk.TOP)

        self.passwordEntry = tk.Entry(self.barra_der, font=("Roboto", 20), show="*")
        self.passwordEntry.pack(side=tk.TOP, fill='both', padx=10, pady=10)

        self.connectButton = tk.Button(self.barra_der, text="Conectar", font=("Roboto", 20), command=self.connect_to_network)
        self.connectButton.pack(side=tk.TOP, fill='both', padx=10, pady=10)

        self.statusLabel = tk.Label(self.barra_der, text="", font=("Roboto", 20), pady=10, bg=COLOR_CUERPO_PRINCIPAL)
        self.statusLabel.pack(side=tk.TOP)

        for network in self.wifi_ssids:
            self.ssids_config(network)

    def ssids_config(self, ssid):
        ssidLabel = tk.Button(self.barra_izq, font=("Roboto", 20), text=ssid, anchor="w", bd=0, fg="#222d33", 
                              command=lambda ssid=ssid: self.select_ssid(ssid), bg=COLOR_CUERPO_PRINCIPAL, pady=10)
        ssidLabel.pack()
        ssidLabel.bind("<Enter>", lambda event: self.on_enter(event, ssidLabel))
        ssidLabel.bind("<Leave>", lambda event: self.on_leave(event, ssidLabel))
        ssidLabel.bind("<FocusIn>", lambda event: self.on_enter(event, ssidLabel))
        ssidLabel.bind("<FocusOut>", lambda event: self.on_leave(event, ssidLabel))

    def select_ssid(self, ssid):
        self.selectedSSIDLabel.config(text="SSID: " + ssid)
        self.selected_ssid = ssid

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg="#dddddd")

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_CUERPO_PRINCIPAL)

    def connect_to_network(self):
        ssid = self.selected_ssid
        password = self.passwordEntry.get()

        success = self.app_logic.connect_to_network(ssid, password)
        if success:
            self.statusLabel.config(text="Conectado", fg="green")
        else:
            self.statusLabel.config(text="Error de conexión", fg="red")
