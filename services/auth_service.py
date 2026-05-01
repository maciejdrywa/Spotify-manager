import os
import webbrowser
import secrets
import hashlib
import base64
import urllib.parse as parse

import requests
from dotenv import load_dotenv

from auth.callback_server import run_server
from models.session_model import SessionModel
from storage.token_storage import TokenStorage


class AuthService:
    def __init__(self):
        # Load keys from .env file
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.redirect_uri = os.getenv("REDIRECT_URI")
        
        # Init token storage with keyring and store session info in ram
        self.storage = TokenStorage()
        self.session = SessionModel(
            refresh_token=self.storage.get_refresh_token()
        )
        
        self.code_verifier = None


    def generate_code_verifier(self):
        # Generate and return secret key
        return secrets.token_urlsafe(64)

    def generate_code_challenge(self, verifier):
        # Hash secret key
        sha256_hash = hashlib.sha256(
            verifier.encode("utf-8")
        ).digest()

        # Change format for url
        code_challenge = base64.urlsafe_b64encode(
            sha256_hash
        ).decode("utf-8")

        # Delete = from the end and return code challenge
        return code_challenge.rstrip("=")
    
    def build_auth_url(self):
        # Generate secret key and modify it to URL format
        self.code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(self.code_verifier)

        # Select params
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
        # run server to get code
        code = run_server()

        if not code:
            raise Exception("Authorization code not received")
        
        return code
        

    def exchange_code_for_tokens(self, code):
        # Url and props for request
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier
        }

        try:
            # Make request
            response = requests.post(
                token_url,
                data=data,
                timeout=10
            )

            # Get respose 
            response.raise_for_status()
            tokens = response.json()

            # Save tokens and time in session
            self.session.set_session(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_in=tokens["expires_in"],
            )
            # Save refresh token localy
            self.storage.save_refresh_token(self.session.refresh_token)

        except requests.RequestException as e:
            print(f"Exchange code error: {e}")
            raise


    def refresh_access_token(self):
        # Url and props for refreshing token
        token_url = "https://accounts.spotify.com/api/token"

        data = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.session.refresh_token
        }

        try:
            # Request build url
            response = requests.post(
                token_url,
                data=data,
                timeout=10
            )

            # Get response
            response.raise_for_status()
            tokens = response.json()

            # Save new access token
            self.session.update_access_token(
                access_token=tokens["access_token"],
                expires_in=tokens["expires_in"],
            )

            # Save new refresh token if it is the new one
            new_refresh_token = tokens.get("refresh_token")
            if new_refresh_token:
                self.session.refresh_token = new_refresh_token
                self.storage.save_refresh_token(
                    self.session.refresh_token
                )

        except requests.RequestException as e:
            print(f"Refreshing token error: {e}")
            raise


    def has_valid_token(self):
        # Check token correctness
        return self.session.is_valid()
            

    def login(self):
        try:
            # Create spotify auth url and execute it
            auth_url = self.build_auth_url()

            webbrowser.open(auth_url)

            # Get code from redirect url
            code = self.wait_for_authorization_code()

            # Excehange code for tokens 
            self.exchange_code_for_tokens(code)

            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
        
    
    def logout(self):
        # Clear keyring storage and RAM session storage 
        self.session.clear()
        self.storage.clear()
        
        
    def get_acces_token(self):
        # Return acces_token if it is avaliable
        if self.has_valid_token():
            return self.session.access_token
        
        # Refresh access_token if refresh_token is avaliable
        if self.session.refresh_token:
            self.refresh_access_token()
            return self.session.access_token
        
        raise Exception("User is not authenticated")
    

    def restore_session(self):
        if not self.session.refresh_token:
            return False

        try:
            # Try to refresh access token
            self.refresh_access_token()
            return True
        except Exception:
            # Clear keyring storage and RAM session storage 
            self.session.clear()
            self.storage.clear()
            return False
        
    
