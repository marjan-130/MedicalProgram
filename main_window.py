from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QFontDatabase, QFont, QPainter
from PyQt6.QtCore import Qt
from login_ui import LoginUI  # Переконайтеся, що цей клас імпортований
from enter_window import EnterWindow
from profile_ui import ProfileWindow  # Імпортуємо вікно профілю користувача
from session import get_session_user_id  # Імпортуємо функцію перевірки сесії

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalCore")
        self.showFullScreen()
        self.background_path = "pictures/backgroundMain.png"
        self.session_active = False  # Змінна для збереження статусу сесії
        self.init_ui()

    def init_ui(self):
        wendy_font, marck_font = self.load_fonts()

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_frame = self.create_center_frame()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(25)

        title = QLabel("VitalCore")
        title.setFont(QFont(wendy_font, 32))
        title.setStyleSheet("color: #0077CC;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.create_buttons(vbox, marck_font)

        vbox.insertWidget(0, title)
        center_frame.setLayout(vbox)

        main_layout.addWidget(center_frame)
        self.setLayout(main_layout)

    def load_fonts(self):
        # Завантаження шрифтів
        wendy_id = QFontDatabase.addApplicationFont("fonts/WendyOne-Regular.ttf")
        marck_id = QFontDatabase.addApplicationFont("fonts/MarckScript-Regular.ttf")
        
        if wendy_id == -1 or marck_id == -1:
            print("Шрифти не були завантажені")
        
        wendy_font = QFontDatabase.applicationFontFamilies(wendy_id)[0]
        marck_font = QFontDatabase.applicationFontFamilies(marck_id)[0]
        return wendy_font, marck_font

    def create_center_frame(self):
        center_frame = QFrame()
        center_frame.setFixedSize(420, 500)
        center_frame.setStyleSheet(""" 
            QFrame {
                background-color: #D1FBFF;
                border-radius: 30px;
                border: none;
            }
        """)
        return center_frame

    def create_buttons(self, vbox, marck_font):
        button_texts = ["Enter", "Login", "Exit"]
        for text in button_texts:
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
            btn.clicked.connect(lambda _, t=text: self.handle_button_click(t))
            vbox.addWidget(btn)

    def handle_button_click(self, text: str):
        if text == "Enter":
            self.show_enter_window()  # Панель здоров'я
        elif text == "Exit":
            QApplication.quit()  # Вихід з програми
        elif text == "Login":
            user_id = get_session_user_id()
            if user_id:  # Якщо сесія активна
                self.show_user_profile_window()  # Відкриваємо профіль користувача
            else:  # Якщо сесія не активна
                self.show_login_window()  # Відкриваємо форму для логіну

    def show_login_window(self):
        """Відкриває вікно для авторизації"""
        self.login_window = LoginUI()  # Передаємо лише LoginUI без self
        self.login_window.show()

    def show_enter_window(self):
        """Відкриває вікно панелі здоров'я"""
        self.enter_window = EnterWindow()
        self.enter_window.show()

    def show_user_profile_window(self):
        """Відкриває вікно профілю користувача"""
        user_id = get_session_user_id()  # Отримуємо ID користувача з сесії
        if user_id:  # Перевірка, чи є ID користувача
            self.user_profile_window = ProfileWindow(user_id)  # Передаємо user_id у конструктор
            self.user_profile_window.show()
        else:
            print("Сесія неактивна. Не вдалося відкрити профіль.")


    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background_path).scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), pixmap)
