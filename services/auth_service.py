import webbrowser
import urllib.parse as urlparse
import os
from dotenv import load_dotenv
from auth.callback_server import run_server


class AuthService():
    def __init__(self):
        load_dotenv()
        self.access_token = None
        self.client_id = os.getenv("CLIENT_ID")
        self.slient_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = os.getenv("REDIRECT_URI")

    def has_token(self):
        return False
    
    def login(self):
        AUTH_URL = "https://accounts.spotify.com/authorize"

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "user-read-private user-read-email",
        }

        url = AUTH_URL + "?" + urlparse.urlencode(params)

        print("AuthService: Logging...")
        print(url)


        webbrowser.open(url)

        code = run_server()

        print("Code: ", code)
