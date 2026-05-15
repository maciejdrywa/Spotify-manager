from PyQt6.QtCore import QThread
from workers.load_playlist_worker import LoadPlaylistWorker

class SpotifyController:
    def __init__(self, view, spotify_service):
        self.view = view
        self.spotify_service = spotify_service

        self._active_tasks = []

    def _start_worker(self, worker, on_finished, on_error=None):
        thread = QThread()

        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.finished.connect(on_finished)

        if on_error is None:
            worker.error.connect(self._on_spotify_error)
        else:
            worker.error.connect(on_error)

        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)

        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        task = {
            "thread": thread,
            "worker": worker
        }

        self._active_tasks.append(task)

        thread.finished.connect(lambda: self._active_tasks.remove(task))

        thread.start()

        
    def _cleanup_thread(self):
        self.thread = None
        self.worker = None

    def _on_spotify_error(self, message):
        print(f"Spotify controller error: {message}")

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
        

    

