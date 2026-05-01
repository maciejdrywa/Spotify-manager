from ui.login_view import LoginView
from ui.home_view import HomeView

from controllers.login_controller import LoginController
from controllers.home_controller import HomeController


class AppController:
    def __init__(self, window, auth_service):
        self.window = window
        self.auth_service = auth_service

        # Try to restore session
        self.auth_service.restore_session()

        # Show home_page if logged in or login_page if not
        if self.auth_service.has_valid_token():
            self.show_home()
        else:
            self.show_login()

    def show_login(self):
        view = LoginView()
        
        # Connect Login controller
        self.login_controller = LoginController(
            view=view,
            auth_service=self.auth_service,
            on_success=self.show_home
        )

        self.window.set_view(view)

    def show_home(self):
        view = HomeView()

        # Connect home controller
        self.home_controller = HomeController(
            view=view,
            auth_service=self.auth_service,
            on_logout=self.show_login
        )

        self.window.set_view(view)