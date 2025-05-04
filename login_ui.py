from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt


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
        # Основний лейаут
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Контейнер для форми
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Логотип та назва
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

        # Заголовок
        title = QLabel("Вхід до системи")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        # Email
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")

        # Пароль
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")

        # Кнопка
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

        # Реєстрація та Забули пароль
        footer_label = QLabel("Не маєте облікового запису?")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_link = QLabel('<a href="#">Зареєструватися</a>')
        register_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_link.setOpenExternalLinks(True)

        forgot_link = QLabel('<a href="#">Забули пароль?</a>')
        forgot_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_link.setOpenExternalLinks(True)

        # Додати елементи до лейауту
        form_layout.addSpacing(10)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(self.message_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(footer_label)
        form_layout.addWidget(register_link)
        form_layout.addWidget(forgot_link)

        main_layout.addWidget(form_widget)
        self.setLayout(main_layout)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        from DataBase import connect_to_database

        conn = connect_to_database()
        if not conn:
            self.message_label.setText("Неможливо підключитися до БД.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE user_name = %s AND hash_password = %s", (username, password))
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
