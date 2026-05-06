import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow

from auth.auth_service import AuthService
from services.spotify_service import SpotifyService

from controllers.app_controller import AppController



def main():
    # Create app
    app = QApplication(sys.argv)

    # Init auth service and Main Window UI 
    auth_service = AuthService()
    spotify_service = SpotifyService(auth_service)
    window = MainWindow()

    # Manipulate state of the app
    AppController(window, auth_service, spotify_service)

    # Show window
    window.show()
    app.exec()


if __name__ == "__main__":
    main()