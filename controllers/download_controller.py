from controllers.worker_controller import BaseWorkerController


class DownloadController(BaseWorkerController):
    def __init__(self, view, download_service):
        super().__init__()
        self.view = view
        self.download_service = download_service


    def download_selected(self):
        selected_tracks_data = self.view.tracks_table.get_checked_rows()

        if len(selected_tracks_data) <= 0:
            return

        self.download_service.download_tracks()
        print(selected_tracks_data)
