from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import QSize, Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalCore")
        
        # Відкриваємо вікно на весь екран
        self.showFullScreen()

        # --- Фон ---
        self.set_background("pictures/backgroundMain.png")  # Шлях до фону

        # --- Центрована панель з кнопками та картинкою ---
        self.init_ui()

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        self.setPalette(palette)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Додавання заголовку
        title = QLabel("VitalCore")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #0077CC;")

        # Додавання кнопок
        btn_enter = QPushButton("Enter")
        btn_login = QPushButton("Login")
        btn_exit = QPushButton("Exit")

        for btn in [btn_enter, btn_login, btn_exit]:
            btn.setFixedSize(200, 40)
            btn.setStyleSheet(""" 
                QPushButton {
                    background-color: #66BFFF;
                    color: white;
                    font-size: 16px;
                    font-style: italic;
                    border-radius: 15px;
                    box-shadow: 2px 2px 4px gray;
                }
                QPushButton:hover {
                    background-color: #55AAEE;
                }
            """)

        # Додавання картинки
        image_label = QLabel()
        pixmap = QPixmap("pictures/image_path.jpg")  # Вкажіть шлях до вашого зображення
        image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Додавання елементів у лейаут
        layout.addWidget(title)
        layout.addWidget(image_label)  # Додано картинку
        layout.addWidget(btn_enter)
        layout.addWidget(btn_login)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Викликаємо show() після showFullScreen()
    sys.exit(app.exec())
