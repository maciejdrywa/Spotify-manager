from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from pathlib import Path


class DownloadService:
    URL = ["https://www.youtube.com/watch?v=PVkVsMbzGso"]

    def __init__(self, settings):
        self.settings = settings


    def _has_local_ffmpeg(self):
        ffmpeg_location = self.settings.get("ffmpeg_location", "ffmpeg/bin")
        ffmpeg_path = Path(ffmpeg_location) / "ffmpeg.exe"

        return ffmpeg_path.exists()
        

    def _build_yt_opts(self):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{self.settings.get('download_path', 'downloads')}/%(title)s.%(ext)s",
            "noplaylist": True,
            "sleep_interval": self.settings.get("sleep_interval", 5),
            "max_sleep_interval": self.settings.get("max_sleep_interval", 15)
        }

        if self._has_local_ffmpeg():
            ffmpeg_location = self.settings.get("ffmpeg_location", "ffmpeg/bin")
            audio_format = self.settings.get("audio_format", "m4a")

            ydl_opts["ffmpeg_location"] = ffmpeg_location

            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
            }]

        if self.settings.get("use_browser_cookies", False):
            cookies_browser = self.settings.get("cookies_browser", "chrome")
            ydl_opts["cookiesfrombrowser"] = (cookies_browser,)

        return ydl_opts

    def _build_urls(self, tracks):
        urls = []

        for track in tracks:
            title = track.get("title")
            artist = track.get("artist")

            url = f"ytsearch1:{title} {artist}"
            urls.append(url)

        return urls


    def download_tracks(self, tracks):
        try:
            yt_opts = self._build_yt_opts()
            urls = self._build_urls(tracks)

            if not urls:
                raise ValueError("No tracks to download")

            with YoutubeDL(yt_opts) as ydl:
                ydl.download(urls)

        except DownloadError as e:
            raise RuntimeError(f"YtDlp downloading error: {e}")

        except FileNotFoundError as e:
            raise RuntimeError(f"Dont find file: {e}")

        except Exception as e:
            raise RuntimeError(f"downloading error: {e}")

