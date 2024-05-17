import sys
import os
import time
import threading
import vlc
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

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

    def play_usb_content(self):
        usb_path = QFileDialog.getExistingDirectory(None, "Seleccionar USB")
        if usb_path:
            self.stop_media_player()
            self.show_usb_content_interface(usb_path)

    def play_vlc_content(self):
        self.stop_media_player()
        media_path = QFileDialog.getOpenFileName(None, "Seleccionar archivo multimedia", "", "Archivos multimedia (*.mp4 *.avi *.mkv);;Todos los archivos (*.*)")[0]
        if media_path:
            self.play_video(media_path)

    def stop_media_player(self):
        if self.media_player:
            self.media_player.stop()
            if self.media_thread:
                self.media_thread.join()
                self.media_thread = None

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

class SmartTVApp(QMainWindow):
    def __init__(self, smart_tv):
        super().__init__()
        self.smart_tv = smart_tv
        self.setWindowTitle("Smart TV Interface")
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black;")

        # Fondo
        self.bg_paths = ["background1.jpg", "background2.jpg", "background3.jpg"]
        self.current_bg_index = 0
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.update_background()
        self.bg_timer = QTimer(self)
        self.bg_timer.timeout.connect(self.update_background)
        self.bg_timer.start(5000)

        # Crear botones de acceso
        buttons_info = [
            {"name": "Netflix", "icon": "netflix.png", "command": self.smart_tv.open_netflix_kiosk},
            {"name": "YouTube", "icon": "youtube.png", "command": self.smart_tv.open_youtube_kiosk},
            {"name": "Google", "icon": "google.png", "command": self.smart_tv.open_google_kiosk},
            {"name": "Reproducir", "icon": "usb.png", "command": self.smart_tv.play_usb_content},
            {"name": "Reproducir con VLC", "icon": "vlc.png", "command": self.smart_tv.play_vlc_content}
        ]

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        for button_info in buttons_info:
            button = QPushButton(button_info["name"])
            button.setIcon(QIcon(button_info["icon"]))
            button.setIconSize(QSize(100, 100))
            button.clicked.connect(button_info["command"])
            button_layout.addWidget(button)

        layout.addLayout(button_layout)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Añadir título en la parte superior izquierda
        title_label = QLabel("Smart TV", self)
        title_label.setStyleSheet("font-size: 30px; color: white;")
        title_label.move(10, 10)

        # Añadir la hora en la parte superior derecha
        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("font-size: 24px; color: white;")
        self.time_label.move(self.width() - 150, 10)
        self.update_time()
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

        # Manejo de teclas
        self.current_button_index = 0
        self.buttons = self.findChildren(QPushButton)
        self.highlight_current_button()

    def resizeEvent(self, event):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.update_background()

    def update_background(self):
        pixmap = QPixmap(self.bg_paths[self.current_bg_index])
        self.bg_label.setPixmap(pixmap.scaled(self.bg_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_paths)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_A:
            self.move_left()
        elif key == Qt.Key_D:
            self.move_right()
        elif key == Qt.Key_W:
            self.move_up()
        elif key == Qt.Key_S:
            self.move_down()
        elif key == Qt.Key_Return:
            self.select_application()
        elif key == Qt.Key_M:
            pass  # Implementar si es necesario
        elif key == Qt.Key_Q:
            if self.smart_tv.media_player:
                self.smart_tv.stop_media_player()
                self.showNormal()  # Mostrar la ventana principal después de salir del reproductor multimedia

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
        selected_button.click()

    def highlight_current_button(self):
        for i, button in enumerate(self.buttons):
            if i == self.current_button_index:
                button.setStyleSheet("background-color: yellow;")
            else:
                button.setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    smart_tv = SmartTV()
    main_window = SmartTVApp(smart_tv)
    main_window.show()
    sys.exit(app.exec_())

