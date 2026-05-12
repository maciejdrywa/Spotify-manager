class PlaylistController:
    def __init__(self, spotify_service):
        self.spotify_service = spotify_service


    def print_user_playlists(self):
        print("Kliknięto: My playlists")

        try:
            playlists = self.spotify_service.get_user_playlists()

            if not playlists:
                print("Nie znaleziono żadnych playlist.")
                return

            print(playlists)

        except Exception as e:
            print(f"PlaylistController error: {e}")
