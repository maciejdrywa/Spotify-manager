from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout


class LoginHeroPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("heroPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(16)

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

        layout.addWidget(logo_label)
        layout.addSpacing(10)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addLayout(chips_row)
