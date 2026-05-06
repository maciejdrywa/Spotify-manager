from PyQt6.QtCore import QTimer

from ui.login_view import LoginView
from ui.home_view import HomeView

from auth.auth_controller import AuthController
from controllers.home_controller import HomeController


class AppController:
    def __init__(self, window, auth_service, spotify_service):
        self.window = window
        self.auth_service = auth_service
        self.spotify_service = spotify_service
        self.auth_controller = None
        self.home_controller = None

        # Try to restore session
        self.auth_service.restore_session()

        # Show home_page if logged in or login_page if not
        if self.auth_service.has_valid_token():
            self.show_home()
        else:
            self.show_login()

    def show_login(self):
        self.teardown_home_controller()
        view = LoginView()

        # Connect auth controller
        self.auth_controller = AuthController(
            view=view,
            auth_service=self.auth_service,
            on_success=self.show_home
        )

        self.window.set_view(view)

    def show_home(self):
        self.teardown_home_controller()
        view = HomeView()

        # Connect home controller
        self.home_controller = HomeController(
            view=view,
            auth_service=self.auth_service,
            spotify_service=self.spotify_service,
            on_logout=self.show_login
        )

        self.window.set_view(view)
        QTimer.singleShot(0, self.home_controller.load_user_profile)

    def teardown_home_controller(self):
        if self.home_controller is None:
            return

        self.home_controller.deactivate()
        self.home_controller = None
