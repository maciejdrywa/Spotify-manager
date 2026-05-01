import keyring
from keyring.errors import PasswordDeleteError


class TokenStorage:
    SERVICE_NAME = "spotify_downloader"
    
    # Save refresh token localy
    def save_refresh_token(self, token):
        keyring.set_password(
            self.SERVICE_NAME,
            "refresh_token",
            token
        )

    # Get refresh token from local machine
    def get_refresh_token(self):
        return keyring.get_password(
            self.SERVICE_NAME,
            "refresh_token"
        )

    # Clear refresh token
    def clear(self):
        try:
            keyring.delete_password(
                self.SERVICE_NAME,
                "refresh_token"
            )
        except PasswordDeleteError:
            pass

