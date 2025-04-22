from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QFontDatabase, QFont, QPainter
from PyQt6.QtCore import Qt
from Alogoritm import handle_button_click  # Імпорт функції обробки кнопок
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalCore")

        self.showFullScreen()
        self.background_path = "pictures/backgroundMain.png"  # шлях до фону

        self.init_ui()

    def init_ui(self):
        # Завантаження шрифтів
        wendy_id = QFontDatabase.addApplicationFont("fonts/WendyOne-Regular.ttf")
        marck_id = QFontDatabase.addApplicationFont("fonts/MarckScript-Regular.ttf")
        wendy_font = QFontDatabase.applicationFontFamilies(wendy_id)[0]
        marck_font = QFontDatabase.applicationFontFamilies(marck_id)[0]

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Центральний блок
        center_frame = QFrame()
        center_frame.setFixedSize(420, 500)
        center_frame.setStyleSheet("""
            QFrame {
                background-color: #D1FBFF;
                border-radius: 30px;
                border: none;
            }
        """)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(25)

        # Заголовок
        title = QLabel("VitalCore")
        title.setFont(QFont(wendy_font, 32))
        title.setStyleSheet("color: #0077CC;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопки
        for text in ["Enter", "Login", "Exit"]:
            btn = QPushButton(text)
            btn.setFixedSize(220, 45)
            btn.setFont(QFont(marck_font, 16))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #66BFFF;
                    color: white;
                    font-style: italic;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #55AAEE;
                }
            """)
            btn.clicked.connect(lambda _, t=text: handle_button_click(t, self))
            vbox.addWidget(btn)

        # Додати заголовок першим
        vbox.insertWidget(0, title)
        center_frame.setLayout(vbox)

        main_layout.addWidget(center_frame)
        self.setLayout(main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background_path).scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
