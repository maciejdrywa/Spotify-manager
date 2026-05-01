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
            images = user.get("images") or []
            avatar_url = images[0].get("url") if images else None
            avatar_data = self.spotify_service.get_image_data(avatar_url)
            profile_data = {
                "username": user.get("display_name") or user.get("id"),
                "email": user.get("email"),
                "avatar_data": avatar_data,
            }
            self.finished.emit(profile_data)

        except Exception as e:
            self.error.emit(str(e))
