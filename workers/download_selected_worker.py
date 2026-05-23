from PyQt6.QtCore import QObject, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, as_completed


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

            if total <= 0:
                self.finished.emit()
                return

            completed = 0

            with ThreadPoolExecutor(max_workers=5) as exe:
                futures = []

                for track in self.tracks:
                    future = exe.submit(self.download_service.download_track, track)
                    futures.append(future)

                for future in as_completed(futures):
                    completed += 1
                    percent = int(completed * 100 / total)
                    self.progress.emit(percent)
                    self.status.emit(f"Downloaded {completed} of {total}")
                    
                
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
