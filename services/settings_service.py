import json
from pathlib import Path


class SettingsService:
    def __init__(self, path="settings.json"):
        self.path = Path(path)

    def default_settings(self):
        return {
            "audio_format": "m4a",
            "download_path": "downloads",
            "use_browser_cookies": False,
            "cookies_browser": "chrome",
            "ffmpeg_location": "ffmpeg/bin",
            "sleep_interval": 5,
            "max_sleep_interval": 15
        }

    def load(self):
        if not self.path.exists():
            settings = self.default_settings()
            self.save(settings)
            return settings

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, settings):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)