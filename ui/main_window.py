from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt

from ui.components.tracks_table import TracksTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify downloader")
        self.setWindowIcon(QIcon("assets/app_icon.png"))
        self.setMinimumSize(1000, 500)

        # Create menu bar
        self.menu = self.menuBar()
        # File menu
        self.file_menu = self.menu.addMenu("File")
        self.setting_action = QAction("Settings", self)
        self.open_downloads_action = QAction("Open downloads folder", self)
        self.exit_action = QAction("Exit", self)

        self.file_menu.addAction(self.setting_action)
        self.file_menu.addAction(self.open_downloads_action)
        self.file_menu.addAction(self.exit_action)
        
        # Account menu
        self.account_menu = self.menu.addMenu("&Account")
        self.login_action = QAction("Login with Spotify", self)
        self.logout_action = QAction("Logout", self)
        self.profile_action = QAction("Profile", self)
        self.refresh_action = QAction("Refresh session", self)

        self.account_menu.addAction(self.login_action)
        self.account_menu.addAction(self.logout_action)
        self.account_menu.addAction(self.profile_action)
        self.account_menu.addAction(self.refresh_action)

        # Spotify menu
        self.spotify_menu = self.menu.addMenu("Spotify")
        self.playlists_action = QAction("Load playlists", self)
        self.liked_action = QAction("Load liked songs", self)
        self.search_playlist_url_action = QAction("Search playlist by URL", self)

        self.spotify_menu.addAction(self.playlists_action)
        self.spotify_menu.addAction(self.liked_action)
        self.spotify_menu.addAction(self.search_playlist_url_action)

        # Download menu
        self.download_menu = self.menu.addMenu("Download")
        self.download_selceted_action = QAction("Download selected", self)
        self.download_playlist_action = QAction("Download playlist", self)
        self.stop_download_action = QAction("Stop download", self)

        self.download_menu.addAction(self.download_selceted_action)
        self.download_menu.addAction(self.download_playlist_action)
        self.download_menu.addAction(self.stop_download_action)

        # Help menu
        self.help_menu = self.menu.addMenu("Help")
        self.github_action = QAction("GitHub / Documentation", self)

        self.help_menu.addAction(self.github_action)

        self.tracks_table = TracksTable()
        self.setCentralWidget(self.tracks_table)






        
        

