from auth.auth_controller import AuthController
from controllers.spotify_controller import SpotifyController
from controllers.download_controller import DownloadController

from auth.auth_service import AuthService

from services.spotify_service import SpotifyService
from services.download_service import DownloadService

import webbrowser


class AppController:
    def __init__(self, window):
        self.window = window
        self.auth_service = AuthService()
        
        # Create Autho Controller
        self.auth_controller = AuthController(
            view=window,
            auth_service=self.auth_service,
            on_success=self.on_login_success,
            on_logout=self.on_logout_success
        )

        self.spotify_service = SpotifyService(
            auth_service=self.auth_service
        )

        self.spotify_controller = SpotifyController(
            view=window,
            spotify_service=self.spotify_service
            )
        
        self.download_service = DownloadService()

        self.download_controller = DownloadController(
            view=window,
            download_service=self.download_service
        )

        # Try to restore session
        self.auth_service.restore_session()

        # Connect menu actions
        self._connect_menu_actions()

        # Update menu state
        self._update_menu_state()



    def _connect_menu_actions(self):
        ## File menu
        # Exit action
        self.window.exit_action.triggered.connect(self.window.close)

        ## Account menu
        # Login action
        self.window.login_action.triggered.connect(self.auth_controller.login)
        #Logout action
        self.window.logout_action.triggered.connect(self.auth_controller.logout)

        ## Spotify menu
        # Playlists action
        self.window.playlists_action.triggered.connect(self.spotify_controller.load_my_playlists)

        # Liked tracks
        self.window.liked_action.triggered.connect(self.spotify_controller.load_my_liked_tracks)

        ## Download menu
        # Download selected action
        self.window.download_selceted_action.triggered.connect(self.download_controller.download_selected)

        ## Help menu
        # Github action
        self.window.github_action.triggered.connect(self.open_github_page)

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
        

    def on_login_success(self):
        self._update_menu_state()

    def on_logout_success(self):
        self._update_menu_state()

    def open_github_page(self):
        webbrowser.open("https://github.com/1maciek90/Spotify-downloader")

    
