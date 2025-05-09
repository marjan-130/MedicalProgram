import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from database_setup import create_database

if __name__ == "__main__":
    create_database()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
