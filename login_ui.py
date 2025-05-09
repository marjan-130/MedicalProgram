from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
import hashlib
from DataBase import connect_to_database, add_user  # Підключення до БД

class LoginWindow(QWidget):
    def __init__(self, login_callback=None):
        super().__init__()
        self.setWindowTitle("Вхід до системи")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #e6f2fb;")
        self.login_callback = login_callback
        self.init_ui()

        field_style = """ color: black; background-color: white; border: 1px solid #ccc; border-radius: 5px; padding: 5px; """
        self.username_input.setStyleSheet(field_style)
        self.password_input.setStyleSheet(field_style)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_widget.setStyleSheet(""" background-color: white; border-radius: 15px; """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo = QLabel("⬜ VitalCore")
        logo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo.setStyleSheet("color: white;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slogan = QLabel("Ваше здоров'я — наш пріоритет")
        slogan.setFont(QFont("Arial", 10))
        slogan.setStyleSheet("color: white;")
        slogan.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_container = QWidget()
        header_container.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
            stop:0 #007bff, stop:1 #0062cc);
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(10, 20, 10, 20)
        header_layout.addWidget(logo)
        header_layout.addWidget(slogan)

        form_layout.addWidget(header_container)

        title = QLabel("Вхід до системи")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")
        self.username_input.setFixedHeight(40)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)

        login_button = QPushButton("Увійти")
        login_button.setFixedHeight(40)
        login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_button.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
            stop:0 #007bff, stop:1 #0062cc);
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        login_button.clicked.connect(self.try_login)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        footer_label = QLabel("Не маєте облікового запису?")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_button = QPushButton("Зареєструватися")
        register_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        register_button.clicked.connect(self.register_user)

        forgot_button = QPushButton("Забули пароль?")
        forgot_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        forgot_button.clicked.connect(self.forgot_password)

        form_layout.addSpacing(10)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(self.message_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(footer_label)
        form_layout.addWidget(register_button)
        form_layout.addWidget(forgot_button)

        main_layout.addWidget(form_widget)
        self.setLayout(main_layout)

    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.message_label.setText("Будь ласка, заповніть усі поля.")
            return

        conn = connect_to_database()
        if not conn:
            self.message_label.setText("Неможливо підключитися до БД.")
            return

        try:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT * FROM users WHERE user_name = ? AND hash_password = ?", (username, hashed_password))
            result = cursor.fetchone()
            if result:
                if self.login_callback:
                    self.login_callback(username)
                self.close()
            else:
                self.message_label.setText("Невірний email або пароль.")
        except Exception as e:
            self.message_label.setText(f"Помилка: {str(e)}")
        finally:
            conn.close()

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.message_label.setText("Будь ласка, заповніть усі поля.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        add_user(username, hashed_password)  # Додаємо нового користувача в базу
        self.message_label.setText("Користувача успішно додано.")

    def forgot_password(self):
        pass  # Реалізувати логіку відновлення паролю
