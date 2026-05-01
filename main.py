import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from services.auth_service import AuthService
from controllers.app_controller import AppController


def main():
    # Create app
    app = QApplication(sys.argv)

    # Init auth service and Main Window UI 
    auth_service = AuthService()
    window = MainWindow()

    # Manipulate state of the app
    AppController(window, auth_service)

    # Show window
    window.show()
    app.exec()


if __name__ == "__main__":
    main()