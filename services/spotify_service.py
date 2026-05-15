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

    def _convert_duration(self, duration_ms):
        total_seconds = duration_ms // 1000
        duration_minutes = total_seconds // 60
        duration_seconds = total_seconds % 60

        duration = f"{duration_minutes}:{duration_seconds:02d}"
        return duration
    
    def _convert_artists(self, artists):
        result = ", ".join(
            artist.get("name", "")
            for artist in artists
            if artist.get("name")
        )
        return result
            


    def get_user_playlists(self):
        data = self._get_api("/me/playlists")

        playlists = []
        

        items = data.get("items", [])

        for item in items:
            id = item.get("id", "")
            name = item.get("name", "")
            owner = item.get("owner", {}).get("display_name", "")
            tracks = self.get_playlist_tracks(id)

            playlist = {
                "id": id,
                "name": name,
                "owner": owner,
                "tracks": tracks
            }

            playlists.append(playlist)

        return playlists
    

    def get_playlist_tracks(self, playlist_id):
        data = self._get_api(f"/playlists/{playlist_id}/items")

        tracks = []

        items = data.get("items", [])

        for item in items:
            id = item.get("item", {}).get("id", "")
            title = item.get("item", {}).get("name", "")

            artists = item.get("item", {}).get("artists", [])
            artist = self._convert_artists(artists)

            duration_ms = int(item.get("item", {}).get("duration_ms", 0))
            duration = self._convert_duration(duration_ms)

            track = {
                "id": id,
                "title": title,
                "artist": artist,
                "duration": duration
            }

            tracks.append(track)

        return tracks
    

    def get_user_liked_songs(self):
        limit = 50
        offset = 0
        tracks = []

        while True:
            data = self._get_api(f"me/tracks?limit={limit}&offset={offset}")

            items = data.get("items", [])

            if not items:
                break

            for item in items:
                track_data = item.get("track", {})

                id = track_data.get("id", "")
                title = track_data.get("name", "")

                artists = track_data.get("artists", [])
                artist = self._convert_artists(artists)

                duration_ms = int(track_data.get("duration_ms", 0))
                duration = self._convert_duration(duration_ms)

                track = {
                    "id": id,
                    "title": title,
                    "artist": artist,
                    "duration": duration 
                }

                tracks.append(track)

            if data.get("next") is None:
                break

            offset += limit

        return tracks

            

            



    



        
