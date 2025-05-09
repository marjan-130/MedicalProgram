from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from login_algorithm import handle_login
from custom_exceptions import EmptyFieldError, ValidationError
from register_ui import RegisterUI


class LoginWindow(QWidget):
    def __init__(self, open_register_callback=None):
        super().__init__()
        self.setWindowTitle("VitalCore — Вхід")
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #0046a3, stop:1 #007bff);
        """)
        self.open_register_callback = open_register_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(30, 40, 30, 20)

        title = QLabel("VitalCore")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Ваше здоров'я — наш пріоритет")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: white;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        form = QWidget()
        form.setStyleSheet("background-color: white; border-radius: 15px;")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)

        header = QLabel("Вхід до системи")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ім’я користувача")
        self.username_input.setFixedHeight(40)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)

        self.login_btn = QPushButton("Увійти")
        self.login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_btn.setFixedHeight(40)
        self.login_btn.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
            stop:0 #007bff, stop:1 #0062cc);
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.login_btn.clicked.connect(self.handle_login)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_hint = QLabel("Не маєте облікового запису?")
        register_hint.setFont(QFont("Arial", 10))
        register_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_btn = QPushButton("Зареєструватися")
        register_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        register_btn.setStyleSheet("""
            color: #0056b3;
            background: transparent;
            border: none;
            font-weight: bold;
            text-decoration: underline;
        """)
        register_btn.clicked.connect(self.open_register)  # Викликаємо open_register

        form_layout.addWidget(header)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_btn)
        form_layout.addWidget(self.message_label)
        form_layout.addWidget(register_hint)
        form_layout.addWidget(register_btn)

        layout.addWidget(form)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        try:
            user = handle_login(username, password)
            self.message_label.setStyleSheet("color: green;")
            self.message_label.setText(f"Вітаємо, {user[1]}!")  # user[1] — це user_name
        except (EmptyFieldError, ValidationError) as e:
            self.message_label.setStyleSheet("color: red;")
            self.message_label.setText(str(e))
        except Exception as e:
            self.message_label.setStyleSheet("color: red;")
            self.message_label.setText(f"Помилка: {str(e)}")

    def open_register(self):
        # Відкриваємо вікно реєстрації
        self.register_window = RegisterUI()
        self.register_window.show()
        self.close()  # Закриваємо вікно логіну
