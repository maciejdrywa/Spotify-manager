import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


from controllers.app_controller import AppController



def main():
    # Create app
    app = QApplication(sys.argv)

    # Init auth service and Main Window UI 
    window = MainWindow()

    # Manipulate state of the app
    window.app_controller = AppController(window)

    # Show window
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
