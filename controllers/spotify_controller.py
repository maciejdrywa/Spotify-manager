class SpotifyController:
    def __init__(self, view, spotify_service):
        self.view = view
        self.spotify_service = spotify_service


    def load_my_playlists(self):
        try:
            playlists_data = self.spotify_service.get_user_playlists()
            self.view.show_playlists(playlists_data)
        except Exception as e:
            print(f"SpotifyController error: {e}")


    

