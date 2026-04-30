from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt


class HomeView(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("homeRoot")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)

        logout_button = QPushButton()
        logout_button.setObjectName("logoutButton")
        logout_button.setText("Wyloguj się")
        logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_button.setMinimumHeight(48)
        logout_button.setMaximumWidth(340)
        logout_button.clicked.connect(self.on_logout_clicked)

        main_layout.addWidget(
            logout_button,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.setLayout(main_layout)

    def on_logout_clicked(self):
        print("Logout clicked")
        self.logout_requested.emit()
