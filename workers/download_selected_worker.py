from PyQt6.QtCore import QObject, pyqtSignal


class DownloadSelectedWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, download_service, tracks):
        super().__init__()
        self.download_service = download_service
        self.tracks = tracks


    def run(self):
        try:
            total = len(self.tracks)

            for index, track in enumerate(self.tracks, start=1):
                self.status.emit(f"Downloading {index} of {total}: {track['title']}")

                self.download_service.download_track(track)

                percent = int(index * 100 / total)
                self.progress.emit(percent)
                
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
