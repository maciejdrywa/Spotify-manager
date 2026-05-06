from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from ui.components.user_profile_card import UserProfileCard


class HomeSidebar(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.profile_card = None
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)

        logo = QLabel("Spotify Downloader")

        btn_home = self.create_nav_button("Home")
        btn_download = self.create_nav_button("Download")
        btn_settings = self.create_nav_button("Settings")
        btn_logout = self.create_nav_button("Logout")
        btn_logout.clicked.connect(self.logout_clicked.emit)

        self.profile_card = UserProfileCard()

        layout.addWidget(logo)
        layout.addWidget(btn_home)
        layout.addWidget(btn_download)
        layout.addWidget(btn_settings)
        layout.addStretch()
        layout.addWidget(self.profile_card)
        layout.addWidget(btn_logout)

    def create_nav_button(self, text):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def set_user_profile(
        self,
        username,
        email,
        avatar_data=None,
        icon_path="assets/unknown_user.jpg",
    ):
        self.profile_card.set_user_profile(
            username=username,
            email=email,
            avatar_data=avatar_data,
            icon_path=icon_path,
        )
