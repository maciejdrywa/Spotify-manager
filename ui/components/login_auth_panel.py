from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget


class LoginAuthPanel(QWidget):
    login_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.button = None
        self.init_ui()

    def init_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(18)

        auth_title = QLabel("Zaloguj się")
        auth_title.setObjectName("authTitle")

        auth_text = QLabel(
            "Kliknięcie otworzy przeglądarkę i rozpocznie autoryzację Twojego konta Spotify."
        )
        auth_text.setObjectName("authText")
        auth_text.setWordWrap(True)

        self.button = QPushButton("Kontynuuj ze Spotify")
        self.button.setObjectName("loginButton")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setMinimumHeight(48)
        self.button.setMaximumWidth(340)
        self.button.clicked.connect(self.login_clicked.emit)

        button_font = QFont()
        button_font.setPointSize(10)
        button_font.setBold(True)
        self.button.setFont(button_font)

        footnote = QLabel("Po udanym logowaniu aplikacja przejdzie dalej automatycznie.")
        footnote.setObjectName("footnote")
        footnote.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(auth_title)
        layout.addWidget(auth_text)
        layout.addSpacing(12)
        layout.addWidget(self.button)
        layout.addWidget(footnote)
        layout.addStretch()
