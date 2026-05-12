class PlaylistController:
    def __init__(self, view, spotify_service):
        self.view = view
        self.spotify_service = spotify_service


    def print_user_playlists(self):

        try:
            playlists = self.spotify_service.get_user_playlists()
            self.view.load_playlists(playlists)

        except Exception as e:
            print(f"PlaylistController error: {e}")
