from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt


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
        self.playlists_action = QAction("My playlists", self)
        self.liked_action = QAction("Liked Songs", self)
        self.search_playlist_url_action = QAction("Search playlist by URL", self)
        self.load_playlists_action = QAction("Load playlist", self)

        self.spotify_menu.addAction(self.playlists_action)
        self.spotify_menu.addAction(self.liked_action)
        self.spotify_menu.addAction(self.search_playlist_url_action)
        self.spotify_menu.addAction(self.load_playlists_action)

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
        self.about_action = QAction("About", self)
        self.github_action = QAction("GitHub / Documentation", self)

        self.help_menu.addAction(self.about_action)
        self.help_menu.addAction(self.github_action)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "Artist", "Duration"])
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 250)
        self.tree.setColumnWidth(2, 200)

        layout.addWidget(self.tree)

        self.download_button = QPushButton("Download selected")

        layout.addWidget(self.download_button)

        self.setCentralWidget(central_widget)

        self.load_playlists()

    def load_playlists(self):
        playlists = [
            {
                "name": "Trening",
                "tracks": [
                    {"title": "Song A", "artist": "Artist 1", "duration": "3:20"},
                    {"title": "Song B", "artist": "Artist 2", "duration": "4:10"},
                ]
            },
            {
                "name": "Chill",
                "tracks": [
                    {"title": "Song C", "artist": "Artist 3", "duration": "2:55"},
                    {"title": "Song D", "artist": "Artist 4", "duration": "3:45"},
                ]
            }
        ]

        self.tree.clear()

        for playlist in playlists:
            playlist_item = QTreeWidgetItem(self.tree)
            playlist_item.setText(0, playlist["name"])
            playlist_item.setText(1, "Playlist")
            playlist_item.setCheckState(0, Qt.CheckState.Unchecked)

            playlist_item.setData(0, Qt.ItemDataRole.UserRole, {
                "type": "playlist",
                "name": playlist["name"]
            })

            for track in playlist["tracks"]:
                track_item = QTreeWidgetItem(playlist_item)
                track_item.setText(0, track["title"])
                track_item.setText(1, track["artist"])
                track_item.setText(2, track["duration"])
                track_item.setCheckState(0, Qt.CheckState.Unchecked)

                track_item.setData(0, Qt.ItemDataRole.UserRole, {
                    "type": "track",
                    "title": track["title"],
                    "artist": track["artist"],
                    "duration": track["duration"],
                    "playlist": playlist["name"]
                })

        self.tree.expandAll()




        
        

