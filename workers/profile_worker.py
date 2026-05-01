from PyQt6.QtCore import QObject, pyqtSignal


class ProfileWorker(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, spotify_service):
        super().__init__()
        self.spotify_service = spotify_service

    def run(self):
        try:
            user = self.spotify_service.get_current_user()
            self.finished.emit(user)

        except Exception as e:
            self.error.emit(str(e))