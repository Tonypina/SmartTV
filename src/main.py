import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app_logic = SmartTVAppLogic()
    app = SmartTVAppGUI(root, app_logic)
    root.mainloop()
