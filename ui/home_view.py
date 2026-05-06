from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from ui.components.home_sidebar import HomeSidebar
from ui.components.playlist_card import PlaylistButton


class HomeView(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sidebar = None
        self.playlists_grid = None
        self.init_ui()

    def init_ui(self):
        self.setObjectName("homeRoot")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = HomeSidebar()
        self.sidebar.logout_clicked.connect(self.on_logout_clicked)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        heading = QLabel("Twoje playlisty")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        playlists_container = QWidget()
        self.playlists_grid = QGridLayout(playlists_container)
        self.playlists_grid.setContentsMargins(0, 0, 0, 0)
        self.playlists_grid.setHorizontalSpacing(16)
        self.playlists_grid.setVerticalSpacing(16)

        scroll_area.setWidget(playlists_container)

        content_layout.addWidget(heading)
        content_layout.addWidget(scroll_area, 1)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_widget, 1)
        self.setLayout(main_layout)

    def on_logout_clicked(self):
        print("Logout clicked")
        self.logout_requested.emit()

    def set_user_profile(
        self,
        username,
        email,
        avatar_data=None,
        icon_path="assets/unknown_user.jpg",
    ):
        self.sidebar.set_user_profile(
            username=username,
            email=email,
            avatar_data=avatar_data,
            icon_path=icon_path,
        )

    def show_playlist_loading_state(self):
        self.clear_playlists()
        self.playlists_grid.addWidget(QLabel("Ładowanie playlist..."), 0, 0)

    def show_playlist_error_state(self):
        self.clear_playlists()
        self.playlists_grid.addWidget(QLabel("Nie udało się załadować playlist."), 0, 0)

    def set_playlists(self, playlists):
        self.clear_playlists()

        if not playlists:
            self.playlists_grid.addWidget(QLabel("Brak playlist do wyświetlenia."), 0, 0)
            return

        for index, playlist in enumerate(playlists):
            row = index // 4
            column = index % 4
            card = PlaylistButton(
                image_path="assets/unknown_user.jpg",
                title=playlist.get("title") or "Unknown playlist",
                subtitle=playlist.get("author") or "Unknown author",
                image_data=playlist.get("image_data"),
            )
            self.playlists_grid.addWidget(card, row, column)

    def clear_playlists(self):
        while self.playlists_grid.count():
            item = self.playlists_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
