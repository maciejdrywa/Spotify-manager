from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout,
    QFrame
)
from PyQt6.QtGui import QFontMetrics, QPixmap
from PyQt6.QtCore import Qt


class PlaylistButton(QFrame):
    TITLE_WIDTH = 140

    def __init__(self, image_path=None, title="", subtitle="", image_data=None):
        super().__init__()

        self.setObjectName("card")
        self.setFixedSize(180, 260)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setSpacing(2)

        self.image = QLabel()
        pixmap = QPixmap()

        if image_data:
            pixmap.loadFromData(image_data)

        if pixmap.isNull() and image_path:
            pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            self.image.setPixmap(
                pixmap.scaled(
                    160, 160,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            self.image.setText("[image]")

        self.title = QLabel()
        self.title.setObjectName("title")
        self.title.setFixedWidth(self.TITLE_WIDTH)
        self.title.setText(self.elide_text(title, self.TITLE_WIDTH))

        self.subtitle = QLabel(subtitle)
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setWordWrap(True)

        layout.addWidget(self.image)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addStretch()

        self.setStyleSheet("""
            #card {
                background: #111;
                border-radius: 14px;
                padding: 10px;
                border: 1px solid #2f2f2f;
            }

            #card:hover {
                background: #1c1c1c;
            }

            #title {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            #subtitle {
                color: #999;
                font-size: 14px;
            }
        """)

        self.setLayout(layout)

    def elide_text(self, text, width):
        metrics = QFontMetrics(self.title.font())
        return metrics.elidedText(
            text or "...",
            Qt.TextElideMode.ElideRight,
            width,
        )

    
    def mousePressEvent(self, event):
        print("klik!")
