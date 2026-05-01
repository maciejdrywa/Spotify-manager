
from PyQt6.QtCore import QThread

from workers.profile_worker import ProfileWorker


class HomeController:
    def __init__(self, view, auth_service, spotify_service, on_logout):
        self.view = view
        self.auth_service = auth_service
        self.spotify_service = spotify_service
        self.on_logout = on_logout
        self.is_active = True
        self.profile_thread = None
        self.profile_worker = None

        self.view.logout_requested.connect(self.logout)

    """
    AUTHENTICATION FUNCTIONS
    """
    
    def logout(self):
        # Logout and show login view
        self.is_active = False
        self.auth_service.logout()
        self.on_logout()

    """
    LOADING PROFILE FUNCTIONS
    """

    def load_user_profile(self):
        if self.is_profile_loading():
            return

        self.show_profile_loading_state()
        self.setup_profile_thread()
        self.start_profile_thread()

    def is_profile_loading(self):
        return self.profile_thread is not None

    def show_profile_loading_state(self):
        self.view.set_user_profile(
            username="Loading...",
            email="Loading profile...",
        )

    def setup_profile_thread(self):
        self.profile_thread = QThread()
        self.profile_worker = ProfileWorker(self.spotify_service)
        self.profile_worker.moveToThread(self.profile_thread)

        self.profile_thread.started.connect(self.profile_worker.run)
        self.profile_worker.finished.connect(self.on_profile_loaded)
        self.profile_worker.error.connect(self.on_profile_error)
        self.profile_worker.finished.connect(self.profile_thread.quit)
        self.profile_worker.error.connect(self.profile_thread.quit)
        self.profile_thread.finished.connect(self.cleanup_profile_thread)

    def start_profile_thread(self):
        self.profile_thread.start()

    def on_profile_loaded(self, profile_data):
        if not self.is_active:
            return

        self.apply_profile_data(profile_data)

    def apply_profile_data(self, profile_data):
        self.view.set_user_profile(
            username=profile_data.get("username"),
            email=profile_data.get("email"),
            avatar_data=profile_data.get("avatar_data"),
        )

    def on_profile_error(self, error_message):
        if not self.is_active:
            return

        print(f"Load profile error: {error_message}")
        self.show_profile_error_state()

    def show_profile_error_state(self):
        self.view.set_user_profile(
            username="Profile unavailable",
            email="Try again later",
        )

    def cleanup_profile_thread(self):
        if self.profile_worker is not None:
            self.profile_worker.deleteLater()
            self.profile_worker = None

        if self.profile_thread is not None:
            self.profile_thread.deleteLater()
            self.profile_thread = None
