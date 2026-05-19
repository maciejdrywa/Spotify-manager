from controllers.worker_controller import BaseWorkerController
from workers.load_playlist_worker import LoadPlaylistWorker
from workers.load_liked_worker import LoadLikedWorker

class SpotifyController(BaseWorkerController):
    def __init__(self, view, spotify_service):
        super().__init__()

        self.view = view
        self.spotify_service = spotify_service
        
    # Download playlist
    def load_my_playlists(self):

        worker = LoadPlaylistWorker(
            spotify_service=self.spotify_service
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_playlists_loaded
        )

    def on_playlists_loaded(self, playlists):
        self.view.tracks_table.show_playlists(playlists)

    # Download liked tracks
    def load_my_liked_tracks(self):
        worker = LoadLikedWorker(
            spotify_service=self.spotify_service
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_liked_tracks_loaded
        )


    def on_liked_tracks_loaded(self, tracks):
        self.view.tracks_table.show_liked_tracks(tracks)




    
        

    

