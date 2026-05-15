from controllers.worker_controller import WorkerController
from workers.load_playlist_worker import LoadPlaylistWorker

class SpotifyController(WorkerController):
    def __init__(self, view, spotify_service):
        super().__init__()

        self.view = view
        self.spotify_service = spotify_service

    def load_my_playlists(self):
        worker = LoadPlaylistWorker(
            spotify_service=self.spotify_service
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_playlists_loaded
        )

    def on_playlists_loaded(self, playlists):
        self.view.show_playlists(playlists)
        

    

