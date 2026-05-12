from PyQt6.QtCore import QTimer

from auth.auth_controller import AuthController
from controllers.playlist_controller import PlaylistController


from auth.auth_service import AuthService

from services.spotify_service import SpotifyService


class AppController:
    def __init__(self, window):
        self.window = window
        self.auth_service = AuthService()
        self.spotify_service = SpotifyService(
            auth_service=self.auth_service
        )

        # Create Autho Controller
        self.auth_controller = AuthController(
            view=window,
            auth_service=self.auth_service,
            on_success=self.on_login_success,
            on_logout=self.on_logout_success
        )
        self.playlist_controller = PlaylistController(
            spotify_service=self.spotify_service
            )

        # Try to restore session
        self.auth_service.restore_session()

        # Connect menu actions
        self._connect_menu_actions()

        # Update menu state
        self._update_menu_state()



    def _connect_menu_actions(self):
        # Login action
        self.window.login_action.triggered.connect(self.auth_controller.login)
        #Logout action
        self.window.logout_action.triggered.connect(self.auth_controller.logout)
        # Exit action
        self.window.exit_action.triggered.connect(self.window.close)
        # Playlists action
        self.window.playlists_action.triggered.connect(
            self.playlist_controller.print_user_playlists
        )
        

    def on_login_success(self):
        self._update_menu_state()

    def on_logout_success(self):
        self._update_menu_state()

    def _update_menu_state(self):
        if self.auth_service.has_valid_token():
            self.window.login_action.setEnabled(False)
            self.window.logout_action.setEnabled(True)
            self.window.profile_action.setEnabled(True)
            self.window.refresh_action.setEnabled(True)
            self.window.spotify_menu.setEnabled(True)
            self.window.download_menu.setEnabled(True)
        else:
            self.window.login_action.setEnabled(True)
            self.window.logout_action.setEnabled(False)
            self.window.profile_action.setEnabled(False)
            self.window.refresh_action.setEnabled(False)
            self.window.spotify_menu.setEnabled(False)
            self.window.download_menu.setEnabled(False)
