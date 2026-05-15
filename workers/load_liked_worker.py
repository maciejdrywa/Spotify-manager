from PyQt6.QtCore import QObject, pyqtSignal

class LoadLikedWorker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, spotify_service):
        super().__init__()
        self.spotify_service = spotify_service


    def run(self):
        try:
            tracks_data = self.spotify_service.get_user_liked_songs()
            self.finished.emit(tracks_data)
        except Exception as e:
            self.error.emit(str(e))