from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ui.components.login_auth_panel import LoginAuthPanel
from ui.components.login_hero_panel import LoginHeroPanel


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

        hero_panel = LoginHeroPanel()
        auth_panel = LoginAuthPanel()
        auth_panel.login_clicked.connect(self.on_login_clicked)

        content_row.addWidget(hero_panel, 7)
        content_row.addWidget(auth_panel, 4)

        outer_layout.addLayout(content_row)
        self.setLayout(outer_layout)

    def on_login_clicked(self):
        print("Kliknięto login")
        self.login_requested.emit()
