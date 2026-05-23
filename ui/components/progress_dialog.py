from PyQt6.QtWidgets import QDialog, QProgressBar, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloading")
        self.setModal(True)
        self.setFixedSize(300, 100)

        self.layout = QVBoxLayout()

        self.status_text = QLabel("Downloading...")
        # self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)


    def set_progress(self, value: int):
        self.progress_bar.setValue(value)
    

    def set_status(self, text: str):
        self.status_text.setText(text)