from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

class TracksTable(QWidget):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "Artist", "Duration"])
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 250)
        self.tree.setColumnWidth(2, 200)
        self.tree.itemChanged.connect(self.on_playlist_checked)

        self.layout.addWidget(self.tree)

        self.setLayout(self.layout)

    def show_playlists(self, playlists):
        self.tree.clear()
        total = len(playlists)

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

        self.progress.emit(100)
        self.status.emit(f"Loaded {total} playlists")

    def show_liked_tracks(self, tracks):
        self.tree.clear()
        total = len(tracks)
        completed = 0

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
        self.progress.emit(100)
        self.status.emit(f"Loaded {total} tracks")


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