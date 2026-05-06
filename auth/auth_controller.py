class AuthController:
    def __init__(self, view, auth_service, on_success=None, on_logout=None):
        self.view = view
        self.auth_service = auth_service
        self.on_success = on_success
        self.on_logout = on_logout

        if hasattr(self.view, "login_requested"):
            self.view.login_requested.connect(self.login)

    def login(self):
        # Try to login
        success = self.auth_service.login()

        # Show home page on succes
        if success and self.on_success:
            self.on_success()

    def logout(self):
        self.auth_service.logout()

        if self.on_logout:
            self.on_logout()
