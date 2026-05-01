from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap


class HomeView(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("homeRoot")

        main_layout = QHBoxLayout()

        # Sidebar container
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(250)

        # Sidebar layout
        left_sidebar = QVBoxLayout(sidebar_widget)
        
        # Sidebar elements
        logo = QLabel("Spotify Downloader")
        btn_home = QPushButton("Home")
        btn_home.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_download = QPushButton("Download")
        btn_download.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_settings = QPushButton("Settings")
        btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_logout = QPushButton("Logout")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.on_logout_clicked)

        # Profile container
        profile_container = QWidget()

        # Profile layout
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.setSpacing(6)

        # Username an email layout
        username_and_email_layout = QVBoxLayout()
        username_and_email_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_and_email_layout.setSpacing(6)

        # Profile elements
        self.user_avatar = QLabel()
        self.user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_label = QLabel("Username")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.email_label = QLabel("email@example.com")
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        username_and_email_layout.addWidget(self.username_label)
        username_and_email_layout.addWidget(self.email_label)

        profile_layout.addWidget(self.user_avatar)
        profile_layout.addLayout(username_and_email_layout)

        self.set_user_profile(
            username="Not loaded",
            email="Not loaded",
        )

        left_sidebar.addWidget(logo)
        left_sidebar.addWidget(btn_home)
        left_sidebar.addWidget(btn_download)
        left_sidebar.addWidget(btn_settings)
        left_sidebar.addStretch()
        left_sidebar.addWidget(profile_container)
        left_sidebar.addWidget(btn_logout)

        # Main content container
        content_widget = QWidget()

        # Main content layout
        content_layout = QVBoxLayout(content_widget)

        # Main content elements
        main_content = QLabel("Main content")

        content_layout.addWidget(main_content)

        main_layout.addWidget(sidebar_widget)
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
        avatar = QPixmap()

        if avatar_data:
            avatar.loadFromData(avatar_data)

        if avatar.isNull():
            avatar = QPixmap(icon_path)

        if not avatar.isNull():
            self.user_avatar.setText("")
            self.user_avatar.setPixmap(
                avatar.scaled(
                    50,
                    50,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.user_avatar.clear()
            self.user_avatar.setText("[icon]")

        self.username_label.setText(username or "Unknown user")
        self.email_label.setText(email or "No email")

