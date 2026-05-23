from controllers.worker_controller import BaseWorkerController
from workers.download_selected_worker import DownloadSelectedWorker
from PyQt6.QtWidgets import QMessageBox
from ui.components.progress_dialog import ProgressDialog


class DownloadController(BaseWorkerController):
    def __init__(self, view, download_service):
        super().__init__()
        self.view = view
        self.download_service = download_service


    def download_selected(self):
        selected_tracks_data = self.view.tracks_table.get_checked_rows()

        if not selected_tracks_data:
            msgBox = QMessageBox()
            msgBox.setText("No tracks selected")
            msgBox.exec()
            return
        
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()
        self.progress_dialog.raise_()
        self.progress_dialog.activateWindow()

        worker = DownloadSelectedWorker(
            download_service=self.download_service,
            tracks=selected_tracks_data
        )

        worker.progress.connect(self.progress_dialog.set_progress)
        worker.status.connect(self.progress_dialog.set_status)

        self._start_worker(
            worker=worker,
            on_finished=self.on_download_finished
        )

    def on_download_finished(self):
        self.progress_dialog.close()

        msgBox = QMessageBox()
        msgBox.setText("Download finished")
        msgBox.exec()
        msgBox.raise_()
        msgBox.activateWindow()
