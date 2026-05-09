from PyQt6.QtCore import QTimer

from auth.auth_controller import AuthController


class AppController:
    def __init__(self, window, auth_service, spotify_service):
        self.window = window
        self.auth_service = auth_service
        self.spotify_service = spotify_service
        self.auth_controller = None
        self.home_controller = None

        # Try to restore session
        self.auth_service.restore_session()

        