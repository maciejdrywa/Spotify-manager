from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class UserProfileCard(QWidget):
    def __init__(self):
        super().__init__()
        self.user_avatar = None
        self.username_label = None
        self.email_label = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)

        username_and_email_layout = QVBoxLayout()
        username_and_email_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_and_email_layout.setSpacing(6)

        self.user_avatar = QLabel()
        self.user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_label = QLabel("Username")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.email_label = QLabel("email@example.com")
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        username_and_email_layout.addWidget(self.username_label)
        username_and_email_layout.addWidget(self.email_label)

        layout.addWidget(self.user_avatar)
        layout.addLayout(username_and_email_layout)

        self.set_user_profile(
            username="Not loaded",
            email="Not loaded",
        )

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
