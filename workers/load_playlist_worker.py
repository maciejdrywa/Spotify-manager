from PyQt6.QtCore import QObject, pyqtSignal

class LoadPlaylistWorker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, spotify_service):
        super().__init__()
        self.spotify_service = spotify_service


    def run(self):
        try:
            playlists_data = self.spotify_service.get_user_playlists()
            self.finished.emit(playlists_data)
        except Exception as e:
            self.error.emit(str(e))

