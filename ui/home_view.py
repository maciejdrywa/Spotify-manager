from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.components.home_sidebar import HomeSidebar


class HomeView(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sidebar = None
        self.init_ui()

    def init_ui(self):
        self.setObjectName("homeRoot")

        main_layout = QHBoxLayout()

        self.sidebar = HomeSidebar()
        self.sidebar.logout_clicked.connect(self.on_logout_clicked)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        main_content = QLabel("Main content")

        content_layout.addWidget(main_content)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_widget)
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
