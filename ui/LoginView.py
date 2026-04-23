from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class LoginView(QWidget):
    login_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("loginRoot")
        self.setStyleSheet(
            """
            QWidget#loginRoot {
                background-color: #171717;
            }
            QFrame#heroPanel {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0f2f21,
                    stop: 1 #0b1f18
                );
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 22px;
            }
            QLabel#eyebrow {
                color: #7ee2a8;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.6px;
            }
            QLabel#title {
                color: #f4f4f5;
                font-size: 30px;
                font-weight: 700;
            }
            QLabel#subtitle {
                color: #c7c7cf;
                font-size: 14px;
                line-height: 1.45;
            }
            QLabel#chip {
                color: #f4f4f5;
                font-size: 12px;
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                padding: 8px 12px;
            }
            QLabel#authTitle {
                color: #fafafa;
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#authText {
                color: #a1a1aa;
                font-size: 13px;
                line-height: 1.45;
            }
            QPushButton#loginButton {
                background-color: #1ed760;
                color: #04130a;
                border: none;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 700;
                padding: 14px 18px;
            }
            QPushButton#loginButton:hover {
                background-color: #35e06f;
            }
            QPushButton#loginButton:pressed {
                background-color: #19bf55;
            }
            QLabel#footnote {
                color: #71717a;
                font-size: 12px;
            }
            """
        )

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(24, 24, 24, 24)

        content_row = QHBoxLayout()
        content_row.setSpacing(22)

        hero_panel = QFrame()
        hero_panel.setObjectName("heroPanel")
        hero_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        hero_layout = QVBoxLayout(hero_panel)
        hero_layout.setContentsMargins(34, 34, 34, 34)
        hero_layout.setSpacing(16)

        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/spotify_logo.png")
        logo_label.setPixmap(
            logo_pixmap.scaled(
                180,
                54,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        eyebrow = QLabel("SPOTIFY DOWNLOADER")
        eyebrow.setObjectName("eyebrow")

        title = QLabel("Zaloguj się do Spotify")
        title.setObjectName("title")
        title.setWordWrap(True)

        subtitle = QLabel(
            "Połącz konto Spotify, aby przejść dalej i pobierać utwory w prostym, "
            "czytelnym interfejsie bez zbędnych kroków."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(10)
        for text in ("Autoryzacja", "Bezpieczne logowanie", "Kilka sekund"):
            chip = QLabel(text)
            chip.setObjectName("chip")
            chips_row.addWidget(chip)
        chips_row.addStretch()

        hero_layout.addWidget(logo_label)
        hero_layout.addSpacing(10)
        hero_layout.addWidget(eyebrow)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        hero_layout.addStretch()
        hero_layout.addLayout(chips_row)

        right_pane = QWidget()
        right_pane.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        right_layout = QVBoxLayout(right_pane)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(18)

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
        self.button.clicked.connect(self.on_login_clicked)

        button_font = QFont()
        button_font.setPointSize(10)
        button_font.setBold(True)
        self.button.setFont(button_font)

        footnote = QLabel("Po udanym logowaniu aplikacja przejdzie dalej automatycznie.")
        footnote.setObjectName("footnote")
        footnote.setWordWrap(True)

        right_layout.addStretch()
        right_layout.addWidget(auth_title)
        right_layout.addWidget(auth_text)
        right_layout.addSpacing(12)
        right_layout.addWidget(self.button)
        right_layout.addWidget(footnote)
        right_layout.addStretch()

        content_row.addWidget(hero_panel, 7)
        content_row.addWidget(right_pane, 4)

        outer_layout.addLayout(content_row)
        self.setLayout(outer_layout)

    def on_login_clicked(self):
        print("Kliknięto login")
        self.login_requested.emit()
