import keyring


class TokenStorage():
    SERVICE_NAME = "spotify_downloader"

    def save_refresh_token(self, token):
        keyring.set_password(
            self.SERVICE_NAME,
            "refresh_token",
            token
        )

    def get_refresh_token(self):
        return keyring.get_password(
            self.SERVICE_NAME,
            "refresh_token"
        )

    def clear(self):
        keyring.delete_password(
            self.SERVICE_NAME,
            "refresh_token"
        )

