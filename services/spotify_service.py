import requests


class SpotifyAuthError(Exception):
    pass


class SpotifyService:
    API_BASE_URL = "https://api.spotify.com/v1"

    def __init__(self, auth_service):
        self.auth_service = auth_service

    def _get_api(self, endpoint):
        access_token = self.auth_service.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        url = f"{self.API_BASE_URL}/{endpoint.lstrip('/')}"

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Spotify API error for '{endpoint}': {e}")
            if getattr(e, "response", None) is not None:
                print(f"Spotify API response: {e.response.text}")
            raise



    def get_user_playlists(self):
        data = self._get_api("/me/playlists")

        playlists = []

        items = data.get("items", [])

        for item in items:
            playlist = {
                "id": item.get("id"),
                "name": item.get("name"),
                "total_tracks": item.get("tracks", {}).get("total", 0),
            }

            playlists.append(playlist)

        return playlists


    



        
