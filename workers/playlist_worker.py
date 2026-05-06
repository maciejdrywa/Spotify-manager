from PyQt6.QtCore import QObject, pyqtSignal

class PlaylistWorker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)


    def __init__(self, spotify_service):
        super().__init__()
        self.spotify_service = spotify_service
        

    def run(self):
        try:
            response = self.spotify_service.get_user_playlists()
            playlists = response.get("items") or []

            playlist_data = []
            for playlist in playlists:
                title = playlist.get("name")

                owner = playlist.get("owner") or {}
                author = owner.get("display_name")


                images = playlist.get("images") or []
                image_url = images[0].get("url") if images else None
                image_data = self.spotify_service.get_image_data(image_url)

                playlist_data.append({
                    "title": title,
                    "author": author,
                    "image_data": image_data

                })

            self.finished.emit(playlist_data)
        except Exception as e:
            self.error.emit(str(e))
