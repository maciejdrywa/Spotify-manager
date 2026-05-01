from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotify downloader")
        self.setWindowIcon(QIcon("assets/app_icon.png"))
        self.setFixedSize(860, 540)

    # Set central widget function
    def set_view(self, view):
        self.setCentralWidget(view)