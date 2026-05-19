from yt_dlp import YoutubeDL


class DownloadService:
    def __init__(self):
        pass

    def download_tracks(self):
        
        URL = ["https://www.youtube.com/watch?v=PVkVsMbzGso"]

        yt_opts = {
            "format": "m4a/bestaudio/best"
        }
        with YoutubeDL(yt_opts) as ydl:
            ydl.download(URL)

