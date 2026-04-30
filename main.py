from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window import MainWindow
from auth.auth_service import AuthService
import sys



def main():
    app = QApplication(sys.argv)
    auth_service = AuthService()
    window = MainWindow(auth_service)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()