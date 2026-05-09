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

        # Set menu enabled functions 
        if self.auth_service.has_valid_token():
            # Account menu
            window.login_action.setEnabled(False)
            window.logout_action.setEnabled(True)
            window.profile_action.setEnabled(True)
            window.refresh_action.setEnabled(True)

            # Spotify menu
            window.spotify_menu.setEnabled(True)

            # Download menu
            window.download_menu.setEnabled(True)
        else:
            # Account menu
            window.login_action.setEnabled(True)
            window.logout_action.setEnabled(False)
            window.profile_action.setEnabled(False)
            window.refresh_action.setEnabled(False)

            # Spotify menu
            window.spotify_menu.setEnabled(False)

            # Download menu
            window.download_menu.setEnabled(False)

        