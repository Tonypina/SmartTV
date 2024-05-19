import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL


class NetworkScreen():

    def __init__(self, panel_principal, app_logic):

        self.wifi_ssids = app_logic.get_wifi_ssids()

        # Crear paneles: barra sup
        self.barra_sup = tk.Frame(panel_principal)
        self.barra_sup.pack(side=tk.TOP, fill=tk.X, expand=False) 
        
        # Crear paneles: barra izquierda
        self.barra_izq = tk.Frame(panel_principal)
        self.barra_izq.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_izq.pack(side=tk.LEFT, fill="both", expand=True) 

        # Crear paneles: barra der
        self.barra_der = tk.Frame(panel_principal)
        self.barra_der.config(bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_der.pack(side=tk.RIGHT, fill="both", expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_sup, text="Configuración de Red")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        self.selectedSSIDLabel = tk.Label(self.barra_der, text="")
        self.selectedSSIDLabel.config(fg="#fff", font=(
            "Roboto", 10), padx=10, width=20)
        self.selectedSSIDLabel.pack(side=tk.TOP, expand=True)

        for network in self.wifi_ssids:
            self.ssids_config(network)

    def ssids_config(self, ssid):
        ssidLabel = tk.Button(self.barra_izq, text=ssid, anchor="w", bd=0, fg="white", command=self.select_ssid(ssid))
        ssidLabel.pack()

    def select_ssid(self, ssid):
        self.selectedSSIDLabel.config(text=ssid)
        self.selectedSSIDLabel.pack(side=tk.TOP, expand=True)
        pass
