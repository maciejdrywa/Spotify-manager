from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.MainWindow import MainWindow
from services.auth_service import AuthService
import sys



def main():
    app = QApplication(sys.argv)
    auth_service = AuthService()
    window = MainWindow(auth_service)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()