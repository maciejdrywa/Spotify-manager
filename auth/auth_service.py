import os
import webbrowser
import secrets
import hashlib
import base64
import urllib.parse as parse
import time

import requests
from dotenv import load_dotenv

from auth.callback_server import run_server
from auth.token_storage import TokenStorage


class AuthService:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.redirect_uri = os.getenv("REDIRECT_URI")

        self.storage = TokenStorage()

        self.refresh_token = self.storage.get_refresh_token()
        self.access_token = None
        self.expires_at = None
        
        self.code_verifier = None


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
    
    def build_auth_url(self):

        self.code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(self.code_verifier)

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "user-read-private user-read-email",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge
        }
        
        return "https://accounts.spotify.com/authorize?" + parse.urlencode(params)
    

    def wait_for_authorization_code(self):
        code = run_server()

        if not code:
            raise Exception("Authorization code not received")
        
        return code
        

    def exchange_code_for_tokens(self, code):
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier
        }

        try:
            response = requests.post(
                token_url,
                data=data,
                timeout=10
            )

            response.raise_for_status()

            tokens = response.json()

            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]

            expires_in = tokens["expires_in"]
            self.expires_at = time.time() + expires_in - 60

            self.storage.save_refresh_token(self.refresh_token)

        except requests.RequestException as e:
            print(f"Exchange code error: {e}")
            raise


    def refresh_access_token(self):
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        try:
            response = requests.post(
                token_url,
                data=data,
                timeout=10
            )

            response.raise_for_status()

            tokens = response.json()

            self.access_token = tokens["access_token"]

            new_refresh_token = tokens.get("refresh_token")
            if new_refresh_token:
                self.refresh_token = new_refresh_token
                self.storage.save_refresh_token(
                    self.refresh_token
                )

            expires_in = tokens["expires_in"]
            self.expires_at = time.time() + expires_in - 60

        except requests.RequestException as e:
            print(f"Refreshing token error: {e}")
            raise


    def has_valid_token(self):
        return (
            self.access_token is not None
            and self.expires_at is not None
            and time.time() < self.expires_at
        )
            

    def login(self):
        try:
            auth_url = self.build_auth_url()

            webbrowser.open(auth_url)

            code = self.wait_for_authorization_code()

            self.exchange_code_for_tokens(code)

            return True
        
        except Exception as e:
            print(f"Login failed: {e}")
            return False
        
    def logout(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.storage.clear()
        
        
    def get_acces_token(self):
        if self.has_valid_token():
            return self.access_token
        
        if self.refresh_token:
            self.refresh_access_token()
            return self.access_token
        
        raise Exception("User is not authenticated")
    
    def restore_session(self):
        if self.refresh_token:
            self.refresh_access_token()
        
    