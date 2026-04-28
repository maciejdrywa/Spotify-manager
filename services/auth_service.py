import os
import webbrowser
import secrets
import hashlib
import base64
import urllib.parse as urlparse

import requests
from dotenv import load_dotenv

from auth.callback_server import run_server
from storage.token_storage import TokenStorage


class AuthService:
    def __init__(self):
        load_dotenv()
        self.storage = TokenStorage()
        self.access_token = None
        self.refresh_token = self.storage.get_refresh_token()

        self.client_id = os.getenv("CLIENT_ID")
        self.redirect_uri = os.getenv("REDIRECT_URI")

        self.code_verifier = None

    

    def has_token(self):
        return self.access_token is not None

    def generate_code_verifier(self):
        return secrets.token_urlsafe(64)

    def generate_code_challenge(self, verifier):
        sha256_hash = hashlib.sha256(
            verifier.encode("utf-8")
        ).digest()

        code_challenge = base64.urlsafe_b64encode(
            sha256_hash
        ).decode("utf-8")

        return code_challenge.rstrip("=")

    def login(self):
        auth_url = "https://accounts.spotify.com/authorize"

        print("AuthService: Logging...")

        # PKCE
        self.code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(
            self.code_verifier
        )

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "user-read-private user-read-email",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge
        }

        url = auth_url + "?" + urlparse.urlencode(params)

        print("Authorization URL:")
        print(url)

        webbrowser.open(url)

        # odbiór code z callback servera
        code = run_server()

        print("Authorization code:", code)

        # wymiana code → token
        self.exchange_code_for_tokens(code)

    def exchange_code_for_tokens(self, code):
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier
        }

        response = requests.post(
            token_url,
            data=data
        )

        response.raise_for_status()

        tokens = response.json()

        self.access_token = tokens["access_token"]
        self.refresh_token = tokens.get("refresh_token")

        self.storage.save_refresh_token(self.refresh_token)

        print("Logged in successfully")
        print("Access token:", self.access_token)

    def refresh_access_token(self):
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(
            token_url,
            data=data
        )

        response.raise_for_status()

        tokens = response.json()

        self.access_token = tokens["access_token"]

        print("Access token refreshed")