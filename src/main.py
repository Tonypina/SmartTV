import tkinter as tk
from smart_tv_app_gui import SmartTVAppGUI
from smart_tv_app_logic import SmartTVAppLogic

if __name__ == "__main__":
    root = tk.Tk()
    app_logic = SmartTVAppLogic()
    app = SmartTVAppGUI(root, app_logic)
    root.mainloop()
