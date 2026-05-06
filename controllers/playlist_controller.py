from PyQt6.QtCore import QThread

from workers.playlist_worker import PlaylistWorker


class PlaylistController:
    def __init__(self, view, spotify_service):
        self.view = view
        self.spotify_service = spotify_service
        self.is_active = True
        self.playlist_thread = None
        self.playlist_worker = None

    def deactivate(self):
        self.is_active = False

    def load_user_playlists(self):
        if self.is_playlist_loading():
            return

        self.show_playlist_loading_state()
        self.setup_playlist_thread()
        self.start_playlist_thread()

    def is_playlist_loading(self):
        return self.playlist_thread is not None

    def show_playlist_loading_state(self):
        if hasattr(self.view, "show_playlist_loading_state"):
            self.view.show_playlist_loading_state()

    def setup_playlist_thread(self):
        self.playlist_thread = QThread()
        self.playlist_worker = PlaylistWorker(self.spotify_service)
        self.playlist_worker.moveToThread(self.playlist_thread)

        self.playlist_thread.started.connect(self.playlist_worker.run)
        self.playlist_worker.finished.connect(self.on_playlists_loaded)
        self.playlist_worker.error.connect(self.on_playlist_error)
        self.playlist_worker.finished.connect(self.playlist_thread.quit)
        self.playlist_worker.error.connect(self.playlist_thread.quit)
        self.playlist_thread.finished.connect(self.cleanup_playlist_thread)

    def start_playlist_thread(self):
        self.playlist_thread.start()

    def on_playlists_loaded(self, playlist_data):
        if not self.is_active:
            return

        self.apply_playlist_data(playlist_data)

    def apply_playlist_data(self, playlist_data):
        if hasattr(self.view, "set_playlists"):
            self.view.set_playlists(playlist_data)

    def on_playlist_error(self, error_message):
        if not self.is_active:
            return

        print(f"Load playlists error: {error_message}")
        self.show_playlist_error_state()

    def show_playlist_error_state(self):
        if hasattr(self.view, "show_playlist_error_state"):
            self.view.show_playlist_error_state()

    def cleanup_playlist_thread(self):
        if self.playlist_worker is not None:
            self.playlist_worker.deleteLater()
            self.playlist_worker = None

        if self.playlist_thread is not None:
            self.playlist_thread.deleteLater()
            self.playlist_thread = None
