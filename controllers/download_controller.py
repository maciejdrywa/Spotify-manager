from controllers.worker_controller import BaseWorkerController
from workers.download_selected_worker import DownloadSelectedWorker
from PyQt6.QtWidgets import QMessageBox


class DownloadController(BaseWorkerController):
    def __init__(self, view, download_service):
        super().__init__()
        self.view = view
        self.download_service = download_service


    def download_selected(self):
        selected_tracks_data = self.view.tracks_table.get_checked_rows()

        if len(selected_tracks_data) <= 0:
            msgBox = QMessageBox()
            msgBox.setText("The document has been modified.")
            msgBox.exec()
            return

        worker = DownloadSelectedWorker(
            download_service=self.download_service,
            tracks=selected_tracks_data
        )

        self._start_worker(
            worker=worker,
            on_finished=self.on_download_selected_finished
        )

    def on_download_selected_finished(self):
        msgBox = QMessageBox()
        msgBox.setText("Pobrano")
        msgBox.exec()
