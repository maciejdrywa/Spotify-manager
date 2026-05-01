

class HomeController:
    def __init__(self, view, auth_service, spotify_service, on_logout):
        self.view = view
        self.auth_service = auth_service
        self.spotify_service = spotify_service
        self.on_logout = on_logout

        self.view.logout_requested.connect(self.logout)

    def logout(self):
        # Logout and show login view
        self.auth_service.logout()
        self.on_logout()

    def load_user_profile(self):
        user = self.spotify_service.get_current_user()

        if user:
            # Parse image and request for image info
            images = user.get("images") or []
            avatar_url = images[0].get("url") if images else None
            avatar_data = self.spotify_service.get_image_data(avatar_url)

            self.view.set_user_profile(
                username=user.get("display_name") or user.get("id"),
                email=user.get("email"),
                avatar_data=avatar_data,
            )
