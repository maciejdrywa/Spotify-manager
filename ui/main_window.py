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

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "Artist", "Duration"])
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 250)
        self.tree.setColumnWidth(2, 200)
        self.tree.itemChanged.connect(self.on_playlist_checked)

        layout.addWidget(self.tree)

        self.setCentralWidget(central_widget)

    def show_playlists(self, playlists):
        self.tree.clear()

        for playlist in playlists:
            playlist_item = QTreeWidgetItem(self.tree)
            playlist_item.setText(0, playlist["name"])
            playlist_item.setText(1, playlist["owner"])
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

    def show_liked_tracks(self, tracks):
        self.tree.clear()

        for track in tracks:
            playlist_item = QTreeWidgetItem(self.tree)
            playlist_item.setText(0, track["title"])
            playlist_item.setText(1, track["artist"])
            playlist_item.setText(2, track["duration"])
            playlist_item.setCheckState(0, Qt.CheckState.Unchecked)

            playlist_item.setData(0, Qt.ItemDataRole.UserRole, {
                "type": "track",
                "title": track["title"],
                "artist": track["artist"],
                "duration": track["duration"]
            })

        self.tree.expandAll()


    def get_checked_rows(self):
        if self.tree.topLevelItemCount() == 0:
            return []

        item = self.tree.topLevelItem(0)
        item_data = item.data(0, Qt.ItemDataRole.UserRole)

        if not item_data:
            return []

        item_type = item_data.get("type")

        if item_type == "track":
            return self.get_checked_tracks()

        if item_type == "playlist":
            return self.get_checked_playlists()

        return []
        

    def get_checked_tracks(self):
        checked_tracks = []

        for i in range(self.tree.topLevelItemCount()):
            track_item = self.tree.topLevelItem(i)

            if track_item.checkState(0) != Qt.CheckState.Checked:
                continue

            track_data = track_item.data(0, Qt.ItemDataRole.UserRole)

            if track_data["type"] == "track":
                checked_tracks.append(track_data)

        return checked_tracks

    def get_checked_playlists(self):
        checked_tracks = []

        for i in range(self.tree.topLevelItemCount()):
            playlist_item = self.tree.topLevelItem(i)

            for j in range(playlist_item.childCount()):
                track_item = playlist_item.child(j)

                if track_item.checkState(0) != Qt.CheckState.Checked:
                    continue

                track_data = track_item.data(0, Qt.ItemDataRole.UserRole)

                if track_data and track_data["type"] == "track":
                    checked_tracks.append(track_data)
            
        return checked_tracks
    
    def on_playlist_checked(self, item, column):
        if column != 0:
            return
        
        data = item.data(0, Qt.ItemDataRole.UserRole)

        if not data:
            return

        if data["type"] != "playlist":
            return

        check_state = item.checkState(0)

        self.tree.blockSignals(True)

        for i in range(item.childCount()):
            track_item = item.child(i)
            track_item.setCheckState(0, check_state)

        self.tree.blockSignals(False)






        
        

