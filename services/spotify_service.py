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
            raise


    def get_user_playlists(self):
        data = self._get_api("/me/playlists")

        playlists = []

        items = data.get("items", [])

        for item in items:
            id = item.get("id")
            name = item.get("name")

            tracks = self.get_playlist_tracks(id)

            playlist = {
                "id": id,
                "name": name,
                "tracks": tracks,
            }

            playlists.append(playlist)

        return playlists
    

    def get_playlist_tracks(self, playlist_id):
        data = self._get_api(f"/playlists/{playlist_id}/items")

        tracks = []

        items = data.get("items", [])

        for item in items:
            id = item.get("item", {}).get("id", "")
            name = item.get("item", {}).get("name", "")

            artists = item.get("item", {}).get("artists", [])
            artist = artists[0].get("name", "")

            duration_ms = int(item.get("item", {}).get("duration_ms", ""))
            duration_minutes = (duration_ms / 1000) // 60
            duration_seconds = (duration_ms / 1000) % 60
            duration = f"duration_minutes:duration"

            track = {
                "id": id,
                "name": name,
                "artist": artist,
                "duration": duration
            }

            tracks.append(track)

        return tracks




    



        
