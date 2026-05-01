

class LoginController():
    def __init__(self, view, auth_service, on_success):
        self.view = view
        self.auth_service = auth_service
        self.on_success = on_success

        self.view.login_requested.connect(self.login)

    def login(self):
        # Try to login
        success = self.auth_service.login()

        # Show home page on succes
        if success:
            self.on_success()