import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import hashlib
from register_ui import RegisterUI  # імпорт перенесено сюди
from profile_ui import ProfileWindow

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизація")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #f0f8ff; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QWidget()
        form.setStyleSheet("background-color: white; border-radius: 15px;")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        title = QLabel("Авторизація")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        self.username_input = self.create_field("Логін")
        self.password_input = self.create_field("Пароль", is_password=True)

        for widget in [self.username_input, self.password_input]:
            form_layout.addWidget(widget)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.message_label)

        login_button = QPushButton("Увійти")
        login_button.setFixedHeight(45)
        login_button.setStyleSheet(
            "background-color: #007bff; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold;"
        )
        login_button.clicked.connect(self.login)

        form_layout.addWidget(login_button)

        self.register_button = QPushButton("Я не маю акаунту")
        self.register_button.setStyleSheet(
            "background-color: transparent; color: #007bff; font-size: 14px;"
        )
        self.register_button.clicked.connect(self.open_register)
        form_layout.addWidget(self.register_button)

        layout.addWidget(form)
        self.setLayout(layout)

    def create_field(self, placeholder, is_password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setEchoMode(QLineEdit.EchoMode.Password if is_password else QLineEdit.EchoMode.Normal)
        field.setFixedHeight(40)
        field.setStyleSheet(
            "background-color: #f5f5f5; border: 1px solid #ccc; border-radius: 6px; padding-left: 10px; font-size: 14px; color: black;"
        )
        return field

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.message_label.setText("Будь ласка, введіть логін та пароль.")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('medical_program.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND hash_password = ?", (username, password_hash))
        user = cursor.fetchone()

        if user:
            self.open_profile(user[0])
        else:
            self.message_label.setText("Невірний логін або пароль.")

    def open_profile(self, user_id):
        self.close()
        self.profile = ProfileWindow(user_id)  # Вам потрібно імпортувати ProfileWindow
        self.profile.show()

    def open_register(self):
        self.close()
        self.register = RegisterUI()  # Реєстраційне вікно
        self.register.show()
