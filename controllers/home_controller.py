


class HomeController:
    def __init__(self, view, auth_service, on_logout):
        self.view = view
        self.auth_service = auth_service
        self.on_logout = on_logout
        self.view.logout_requested.connect(self.logout)

    def logout(self):
        # Logout and show login view
        self.auth_service.logout()
        self.on_logout()
