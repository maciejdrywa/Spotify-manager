import time


class SessionModel:
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
        expires_at=None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def set_session(self, access_token, refresh_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = time.time() + expires_in - 60

    def update_access_token(self, access_token, expires_in):
        self.access_token = access_token
        self.expires_at = time.time() + expires_in - 60

    def clear(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

    def is_valid(self):
        return (
            self.access_token is not None
            and self.expires_at is not None
            and time.time() < self.expires_at
        )
