from controllers.profile_controller import ProfileController
from controllers.playlist_controller import PlaylistController
from auth.auth_controller import AuthController


class HomeController:
    def __init__(self, view, auth_service, spotify_service, on_logout):
        self.view = view
        self.auth_controller = AuthController(
            view=view,
            auth_service=auth_service,
            on_logout=on_logout,
        )
        self.profile_controller = ProfileController(
            view=view,
            spotify_service=spotify_service,
        )
        self.playlist_controller = PlaylistController(
            view=view,
            spotify_service=spotify_service,
        )
        self.view.logout_requested.connect(self.handle_logout)

    def handle_logout(self):
        self.profile_controller.deactivate()
        self.playlist_controller.deactivate()
        self.auth_controller.logout()

    def load_home_data(self):
        self.profile_controller.load_user_profile()
        self.playlist_controller.load_user_playlists()

    def deactivate(self):
        self.profile_controller.deactivate()
        self.playlist_controller.deactivate()
