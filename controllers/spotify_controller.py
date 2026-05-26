from PyQt6.QtWidgets import QMessageBox
from controllers.worker_controller import BaseWorkerController
from workers.load_playlist_worker import LoadPlaylistWorker
from workers.load_liked_worker import LoadLikedWorker
from ui.components.progress_dialog import ProgressDialog

class SpotifyController(BaseWorkerController):
    def __init__(self, view, spotify_service):
        super().__init__()

        self.view = view
        self.spotify_service = spotify_service
        
    # Download playlist
    def load_my_playlists(self):

        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()
        self.progress_dialog.raise_()
        self.progress_dialog.activateWindow()

        self.view.tracks_table.progress.connect(self.progress_dialog.set_progress)
        self.view.tracks_table.status.connect(self.progress_dialog.set_status)

        worker = LoadPlaylistWorker(
            spotify_service=self.spotify_service
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_playlists_loaded
        )

    def on_playlists_loaded(self, playlists):
        self.view.tracks_table.show_playlists(playlists)
        self.progress_dialog.finish("Playlists tracks loaded")

    # Download liked tracks
    def load_my_liked_tracks(self):

        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()
        self.progress_dialog.raise_()
        self.progress_dialog.activateWindow()

        self.view.tracks_table.progress.connect(self.progress_dialog.set_progress)
        self.view.tracks_table.status.connect(self.progress_dialog.set_status)

        worker = LoadLikedWorker(
            spotify_service=self.spotify_service
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_liked_tracks_loaded
        )


    def on_liked_tracks_loaded(self, tracks):
        self.view.tracks_table.show_liked_tracks(tracks)
        self.progress_dialog.finish("Liked tracks loaded")




    
        

    

