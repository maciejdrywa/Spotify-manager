from PyQt6.QtWidgets import QDialog, QProgressBar, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloading")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.setFixedSize(300, 130)

        self.can_close = False

        self.layout = QVBoxLayout()

        self.status_text = QLabel("Downloading...")
        self.layout.addWidget(self.status_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.ok_button = QPushButton("OK")
        self.ok_button.hide()
        self.ok_button.clicked.connect(self.close_dialog)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(400)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def set_progress(self, value: int):
        value = max(0, min(100, value))

        self.progress_animation.stop()
        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(value)
        self.progress_animation.start()

    def set_status(self, text: str):
        self.status_text.setText(text)

    def finish(self, text: str = "Done"):
        self.setWindowTitle("Finished")
        self.set_status(text)
        self.set_progress(100)

        self.can_close = True
        self.ok_button.show()
        self.ok_button.setFocus()

    def close_dialog(self):
        self.can_close = True
        self.close()

    def closeEvent(self, event):
        if self.can_close:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and not self.can_close:
            event.ignore()
        else:
            super().keyPressEvent(event)