from PyQt6.QtWidgets import QMainWindow
from ui.LoginView import LoginView
from ui.HomeView import HomeView


class MainWindow(QMainWindow):
    def __init__(self, auth_service):
        super().__init__()
        self.setWindowTitle("Spotify downloader")
        self.setFixedSize(860, 540)

        self.auth_service = auth_service

        if self.auth_service.has_token():
            self.show_home()
        else:
            self.show_login()

    def show_login(self):
        self.login_view = LoginView()
        self.setCentralWidget(self.login_view)

        self.login_view.login_requested.connect(self.handle_login)

    def show_home(self):
        self.home_view = HomeView()
        self.setCentralWidget(self.home_view)

    def handle_login(self):
        print("klik login")

        self.auth_service.login()

        self.show_home()
