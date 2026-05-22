from PyQt6.QtCore import QObject, pyqtSignal


class DownloadSelectedWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, download_service, tracks):
        super().__init__()
        self.download_service = download_service
        self.tracks = tracks


    def run(self):
        try:
            self.download_service.download_tracks(self.tracks)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
