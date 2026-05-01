import requests


class SpotifyAuthError(Exception):
    pass


class SpotifyService:
    def __init__(self, auth_service):
        self.auth_service = auth_service


    def get_current_user(self):
        # Get acces token
        access_token = self.auth_service.get_access_token()

        # Create headers
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            # Make request
            response = requests.get(
                "https://api.spotify.com/v1/me",
                headers=headers,
                timeout=10
            )

            # Get response
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            print(f"Get user error: {e}")
            raise


    def get_image_data(self, image_url):
        if not image_url:
            return None

        try:
            # Try download onfo about user image
            response = requests.get(
                image_url,
                timeout=10
            )
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Get image error: {e}")
            return None



        
