from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from ui.login_view import LoginView
from ui.home_view import HomeView


class MainWindow(QMainWindow):
    def __init__(self, auth_service):
        super().__init__()
        self.setWindowTitle("Spotify downloader")
        self.setWindowIcon(QIcon("assets/app_icon.png"))
        self.setFixedSize(860, 540)

        self.auth_service = auth_service
        self.auth_service.restore_session()

        if self.auth_service.has_valid_token():
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

        self.home_view.logout_requested.connect(self.handle_logout)

    def handle_login(self):
        try:
            success  = self.auth_service.login()

            if success :
                self.show_home()
        except Exception as e:
            print(f"Login failed: {e}")

    def handle_logout(self):
        self.auth_service.logout()
        self.show_login()
